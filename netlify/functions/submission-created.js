/**
 * submission-created.js
 * Netlify event-triggered function. Runs automatically on every Netlify Forms
 * submission for this site. Builds a question-and-answer PDF of the intake and
 * safety screen and emails it to the practice.
 *
 * Environment variables (set in Netlify UI > Site configuration > Environment variables):
 *   GMAIL_USER          - Google Workspace address the mail is sent from
 *   GMAIL_APP_PASSWORD  - App password generated for that account
 *   DESTINATION_EMAIL   - Where the PDF goes (optional; defaults to GMAIL_USER)
 */

const { PDFDocument, rgb } = require("pdf-lib");
const fontkit = require("@pdf-lib/fontkit");
const nodemailer = require("nodemailer");
const MANROPE = require("./fonts.js");

/* ------------------------------------------------------------------ */
/* Question dictionary - must mirror the wording on the live form      */
/* ------------------------------------------------------------------ */

const SECTIONS = [
  {
    title: "About you and your matter",
    items: [
      { key: "client_name", q: "Your full name" },
      { key: "matter_type", q: "What is your matter about?" },
    ],
  },
  {
    title: "How you're doing right now (1 = not at all, 5 = neutral, 10 = absolutely)",
    items: [
      { key: "w1", q: "The separation has been weighing on me more than I can manage at the moment.", scale: true },
      { key: "w2", q: "Lately I've felt more anxious, angry or low than usual.", scale: true },
      { key: "w3", q: "I feel like I'm facing all of this largely on my own.", scale: true },
      { key: "w4", q: "When the other party and I try to sort things out, it usually turns into conflict.", scale: true, gate: "contact" },
    ],
  },
  {
    title: "Contact with the other party",
    items: [
      { key: "contact", q: "Have you had any contact with the other party in the last six months or so?" },
    ],
  },
  {
    title: "Your safety",
    items: [
      { key: "s_safe", q: "Are you ever concerned for your own safety because of the other party (or anyone connected to them)?", risk: true },
      { key: "s_react", q: "Are you worried about how the other party might react if they're unhappy with the outcome of this process?", risk: true, gate: "contact" },
      { key: "s_phys", q: "In the last year, has the other party physically hurt you, or used force to make you do something you didn't want to do?", risk: true },
      { key: "s_threat", q: "Has the other party ever threatened to harm you, your children, themselves, or anyone else?", risk: true },
      { key: "s_control", q: "Does the other party try to control things like your money, where you go, or who you see?", risk: true },
      { key: "s_stalk", q: "Has the other party followed, monitored or tracked you, in person or through your phone, accounts or social media?", risk: true },
      { key: "s_order", q: "Have the police ever been involved, or has any intervention or protection order ever been made, because of the other party's behaviour?", risk: true },
      { key: "s_order_now", q: "Is an order currently in place?", risk: true, sub: "s_order" },
      { key: "s_weapon", q: "Does the other party have access to a firearm or other weapon?", risk: true },
      { key: "s_escalate", q: "Lately, are any of these things happening more often, or getting worse?", risk: true },
    ],
  },
  {
    title: "Your children",
    childrenOnly: true,
    items: [
      { key: "c_safe", q: "Do you have any concerns about your children's safety with the other parent, or anyone else who cares for them?", risk: true },
      { key: "c_exposed", q: "Have your children ever seen or heard frightening conflict or violence at home?", risk: true },
      { key: "c_cp", q: "Has child protection ever been involved with your family?", risk: true },
      { key: "c_cp_now", q: "Is anything currently open or ongoing?", risk: true, sub: "c_cp" },
      { key: "c_withhold", q: "Has either parent ever threatened to take or keep the children outside the agreed arrangement?", risk: true, gate: "contact" },
    ],
  },
  {
    title: "A couple about you",
    items: [
      { key: "o_concern", q: "Has anyone ever raised a concern about your behaviour towards the other party or your children?", risk: true },
      { key: "o_order", q: "Is there an intervention or protection order currently in place against you?", risk: true },
    ],
  },
  {
    title: "How you've been coping",
    items: [
      { key: "sh", q: "Have things ever felt so overwhelming that you've thought about harming yourself?", risk: true },
      { key: "sh_now", q: "Is that something you've felt recently?", risk: true, sub: "sh" },
    ],
  },
  {
    title: "In their own words",
    items: [
      { key: "what_would_help", q: "What would help you feel safe and able to take part?", freeText: true },
      { key: "anything_else", q: "Anything else you think we should know?", freeText: true },
    ],
  },
];

/* ------------------------------------------------------------------ */
/* Answer formatting                                                   */
/* ------------------------------------------------------------------ */

function pretty(value, item) {
  if (value === undefined || value === null || String(value).trim() === "") return null;
  const v = String(value).trim();
  if (item && item.scale) return v + " / 10";
  const map = {
    yes: "Yes",
    no: "No",
    defer: "Would rather discuss in session",
    unsure: "Not sure",
    parenting: "Parenting",
    property: "Property only",
    both: "Parenting and property",
  };
  return map[v.toLowerCase()] || v;
}

function isApplicable(item, data) {
  if (item.gate === "contact" && data.contact !== "yes") return false;
  if (item.sub && data[item.sub] !== "yes") return false;
  return true;
}

function sectionApplicable(section, data) {
  if (section.childrenOnly && data.matter_type === "property") return false;
  return true;
}

function buildFlags(data) {
  const flags = [];
  for (const section of SECTIONS) {
    if (!sectionApplicable(section, data)) continue;
    for (const item of section.items) {
      if (!item.risk || !isApplicable(item, data)) continue;
      const v = (data[item.key] || "").toLowerCase();
      if (v === "yes" || v === "defer" || v === "unsure") {
        flags.push({ q: item.q, a: pretty(v, item) });
      }
    }
  }
  // High wellbeing scores are a check-in prompt, listed after safety flags.
  for (const key of ["w1", "w2", "w3", "w4"]) {
    const n = parseInt(data[key], 10);
    if (!isNaN(n) && n >= 8) {
      const item = SECTIONS[1].items.find((i) => i.key === key);
      flags.push({ q: "Wellbeing check-in: " + item.q, a: n + " / 10" });
    }
  }
  return flags;
}

/* ------------------------------------------------------------------ */
/* PDF generation - brand tokens from base.css                         */
/* ------------------------------------------------------------------ */

const A4 = { w: 595.28, h: 841.89 };
const MARGIN = 52;

const CHARCOAL  = rgb(0.173, 0.157, 0.145); // #2C2825
const MID       = rgb(0.478, 0.435, 0.396); // #7A6F65
const OCHRE     = rgb(0.769, 0.529, 0.227); // #C4873A
const TERRA     = rgb(0.659, 0.361, 0.196); // #A85C32
const OCHRE_PALE= rgb(0.976, 0.949, 0.910); // #F9F2E8
const DUST      = rgb(0.949, 0.929, 0.894); // #F2EDE4
const DUST_3    = rgb(0.847, 0.808, 0.753); // #D8CEC0

// Handshake mark, lucide icon as used in the site nav (24x24 viewBox, stroked).
const MARK_PATHS = [
  "m11 17 2 2a1 1 0 1 0 3-3",
  "m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4",
  "m21 3 1 11h-2",
  "M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3",
  "M3 4h8",
];

function wrap(text, font, size, maxWidth) {
  const paragraphs = String(text).replace(/\r/g, "").split("\n");
  const lines = [];
  for (const para of paragraphs) {
    const words = para.split(/\s+/).filter(Boolean);
    if (!words.length) { lines.push(""); continue; }
    let line = "";
    for (const word of words) {
      const test = line ? line + " " + word : word;
      if (font.widthOfTextAtSize(test, size) > maxWidth && line) {
        lines.push(line);
        line = word;
      } else {
        line = test;
      }
    }
    if (line) lines.push(line);
  }
  return lines.length ? lines : [""];
}

async function buildPdf(data, receivedAt) {
  const doc = await PDFDocument.create();
  doc.registerFontkit(fontkit);
  const font  = await doc.embedFont(MANROPE.regular, { subset: true });
  const bold  = await doc.embedFont(MANROPE.bold, { subset: true });
  const black = await doc.embedFont(MANROPE.extrabold, { subset: true });

  doc.setTitle("Intake and Safety Screen - " + (data.client_name || "Unnamed"));
  doc.setCreator("onlinefdr.com.au");
  doc.setProducer("onlinefdr.com.au");

  const width = A4.w - MARGIN * 2;
  let page = doc.addPage([A4.w, A4.h]);
  let y = A4.h - MARGIN;

  function ensure(space) {
    if (y - space < MARGIN + 26) {
      page = doc.addPage([A4.w, A4.h]);
      y = A4.h - MARGIN;
      return true;
    }
    return false;
  }

  function drawLines(lines, x, size, usedFont, color, gap) {
    for (const ln of lines) {
      ensure(size + 2);
      if (ln) page.drawText(ln, { x, y, size, font: usedFont, color });
      y -= size + (gap === undefined ? 3 : gap);
    }
  }

  /* ---------- Masthead ---------- */
  const markScale = 26 / 24;
  for (const d of MARK_PATHS) {
    page.drawSvgPath(d, {
      x: MARGIN, y: y + 8, scale: markScale,
      borderColor: OCHRE, borderWidth: 1.9, borderLineCap: 1,
    });
  }
  let bx = MARGIN + 36;
  page.drawText("online", { x: bx, y: y - 6, size: 15, font: black, color: CHARCOAL });
  bx += black.widthOfTextAtSize("online", 15);
  page.drawText("fdr", { x: bx, y: y - 6, size: 15, font: black, color: OCHRE });
  bx += black.widthOfTextAtSize("fdr", 15);
  page.drawText(".com.au", { x: bx, y: y - 6, size: 15, font: black, color: CHARCOAL });
  page.drawText("Accredited Online FDR", { x: MARGIN + 36, y: y - 18, size: 7.5, font, color: MID });

  const contact = "1800 957 253   |   hello@onlinefdr.com.au";
  page.drawText(contact, {
    x: A4.w - MARGIN - font.widthOfTextAtSize(contact, 8),
    y: y - 6, size: 8, font, color: MID,
  });
  y -= 34;
  page.drawLine({ start: { x: MARGIN, y }, end: { x: A4.w - MARGIN, y }, thickness: 2, color: OCHRE });
  y -= 26;

  /* ---------- Title ---------- */
  page.drawText("Intake and Safety Screen", { x: MARGIN, y, size: 20, font: black, color: CHARCOAL });
  const badge = "CONFIDENTIAL";
  const bw = bold.widthOfTextAtSize(badge, 7.5) + 16;
  page.drawRectangle({ x: A4.w - MARGIN - bw, y: y - 2, width: bw, height: 18, color: TERRA, borderRadius: 3 });
  page.drawText(badge, { x: A4.w - MARGIN - bw + 8, y: y + 3, size: 7.5, font: bold, color: rgb(1, 1, 1) });
  y -= 16;
  page.drawText("Completed by one party before their intake session. Not shared with the other party.",
    { x: MARGIN, y, size: 8.5, font, color: MID });
  y -= 20;

  /* ---------- Meta panel ---------- */
  const meta = [
    ["Client", data.client_name || "Not provided"],
    ["Matter type", pretty(data.matter_type) || "Not provided"],
    ["Received", receivedAt],
  ];
  const panelH = meta.length * 16 + 14;
  page.drawRectangle({ x: MARGIN, y: y - panelH + 10, width, height: panelH, color: DUST });
  let my = y - 2;
  for (const [label, value] of meta) {
    page.drawText(label, { x: MARGIN + 12, y: my, size: 9, font: bold, color: MID });
    page.drawText(String(value), { x: MARGIN + 96, y: my, size: 9, font, color: CHARCOAL });
    my -= 16;
  }
  y -= panelH + 14;

  /* ---------- Flag summary ---------- */
  const flags = buildFlags(data);
  if (flags.length) {
    const rows = flags.map((f) => wrap(f.q + "  >  " + f.a, font, 9, width - 42));
    const boxH = rows.reduce((a, r) => a + r.length * 12, 0) + 34;
    ensure(boxH);
    page.drawRectangle({ x: MARGIN, y: y - boxH + 12, width, height: boxH, color: OCHRE_PALE });
    page.drawRectangle({ x: MARGIN, y: y - boxH + 12, width: 3, height: boxH, color: OCHRE });
    let fy = y;
    page.drawText("For review before session (" + flags.length + ")",
      { x: MARGIN + 16, y: fy, size: 10.5, font: black, color: TERRA });
    fy -= 16;
    rows.forEach((lines) => {
      page.drawText("-", { x: MARGIN + 16, y: fy, size: 9, font: bold, color: OCHRE });
      for (const ln of lines) {
        page.drawText(ln, { x: MARGIN + 26, y: fy, size: 9, font, color: CHARCOAL });
        fy -= 12;
      }
    });
    y -= boxH + 16;
  } else {
    const boxH = 30;
    ensure(boxH);
    page.drawRectangle({ x: MARGIN, y: y - boxH + 12, width, height: boxH, color: DUST });
    page.drawRectangle({ x: MARGIN, y: y - boxH + 12, width: 3, height: boxH, color: DUST_3 });
    page.drawText("No safety items flagged", { x: MARGIN + 16, y, size: 10.5, font: black, color: CHARCOAL });
    page.drawText("All safety questions answered No, or not applicable to this matter.",
      { x: MARGIN + 16, y: y - 13, size: 8.5, font, color: MID });
    y -= boxH + 16;
  }

  /* ---------- Transcript ---------- */
  for (const section of SECTIONS) {
    const applicable = sectionApplicable(section, data);
    ensure(52);
    const titleLines = wrap(section.title, black, 11, width);
    drawLines(titleLines, MARGIN, 11, black, CHARCOAL, 4);
    y += 2;
    page.drawLine({ start: { x: MARGIN, y }, end: { x: MARGIN + 34, y }, thickness: 1.5, color: OCHRE });
    y -= 14;

    if (!applicable) {
      page.drawText("Not shown to this client (matter type: " + (pretty(data.matter_type) || "unknown") + ").",
        { x: MARGIN, y, size: 9, font, color: MID });
      y -= 22;
      continue;
    }

    for (const item of section.items) {
      const shown = isApplicable(item, data);
      const answer = pretty(data[item.key], item);
      const x = MARGIN + (item.sub ? 18 : 0);
      const w = width - (item.sub ? 18 : 0);

      const qLines = wrap(item.q, font, 9, w);
      ensure(qLines.length * 12 + 26);

      if (item.sub) {
        page.drawRectangle({ x: MARGIN + 6, y: y - qLines.length * 12 - 4, width: 1.5, height: qLines.length * 12 + 16, color: DUST_3 });
      }
      drawLines(qLines, x, 9, font, MID, 3);

      let aText, aColor = CHARCOAL, aFont = bold;
      const v = String(data[item.key] || "").toLowerCase();
      if (!shown) { aText = "Not applicable, question not shown"; aColor = MID; aFont = font; }
      else if (answer === null) { aText = "Not answered"; aColor = MID; aFont = font; }
      else {
        aText = answer;
        if (v === "yes" || v === "defer" || v === "unsure") aColor = TERRA;
      }
      const aLines = wrap(aText, aFont, item.freeText ? 9.5 : 10, w);
      drawLines(aLines, x, item.freeText ? 9.5 : 10, aFont, aColor, 3);
      y -= 10;
    }
    y -= 6;
  }

  /* ---------- Footer ---------- */
  const pages = doc.getPages();
  pages.forEach((p, i) => {
    p.drawLine({ start: { x: MARGIN, y: 42 }, end: { x: A4.w - MARGIN, y: 42 }, thickness: 0.75, color: DUST_3 });
    p.drawText("Intake and Safety Screen  |  Confidential  |  " + (data.client_name || "Unnamed"),
      { x: MARGIN, y: 30, size: 7.5, font, color: MID });
    const pn = "Page " + (i + 1) + " of " + pages.length;
    p.drawText(pn, { x: A4.w - MARGIN - font.widthOfTextAtSize(pn, 7.5), y: 30, size: 7.5, font, color: MID });
  });

  return Buffer.from(await doc.save());
}
/* ------------------------------------------------------------------ */
/* Handler                                                             */
/* ------------------------------------------------------------------ */

const FEE_GUIDE_URL = "https://onlinefdr.com.au/downloads/onlinefdr-fee-guide.pdf";
const BOOKING_URL = "https://go.acr.fit/widget/bookings/book-consult-call-with-kevin";

function makeTransport() {
  return nodemailer.createTransport({
    host: "smtp.gmail.com",
    port: 465,
    secure: true,
    auth: { user: process.env.GMAIL_USER, pass: process.env.GMAIL_APP_PASSWORD },
  });
}

function prettyMatter(v) {
  if (!v) return null;
  const map = {
    "parenting": "Parenting",
    "financial settlement": "Financial settlement",
    "financial": "Financial settlement",
    "parenting + financial": "Parenting and financial",
    "parenting and financial": "Parenting and financial",
    "section 60i certificate only": "Section 60I certificate only",
    "divorce application": "Divorce application",
  };
  return map[String(v).trim().toLowerCase()] || v;
}

function esc(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function leadEmailHtml(first) {
  return [
    '<div style="font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.55;color:#2C2825;max-width:560px">',
    "<p>Hi " + esc(first) + ",</p>",
    "<p>Thanks for getting in touch. Here's what you need to know: most separations don't need to go anywhere near a courtroom, and the ones that do cost tens of thousands of dollars and drag on for a year or more.</p>",
    "<p>There's a better way. Family Dispute Resolution resolves most matters in weeks, for a fraction of the cost, with you and the other party keeping control of the outcome instead of handing it to a judge.</p>",
    '<p>See exactly what it costs: <a href="' + FEE_GUIDE_URL + '" style="color:#A85C32">our fee guide</a>.</p>',
    "<p>You pay for each stage as you reach it. No hourly billing, no surprises, and the first step, a discovery call to see if we're the right fit, is free.</p>",
    '<p style="margin:22px 0"><a href="' + BOOKING_URL + '" style="background:#C4873A;color:#FDFAF6;text-decoration:none;padding:12px 22px;border-radius:6px;font-weight:bold;display:inline-block">Book your free discovery call</a></p>',
    '<p>Or call <strong>1800 957 253</strong>. The sooner you start, the sooner this is behind you.</p>',
    '<p style="margin-top:26px">Kind regards,</p>',
    '<table cellpadding="0" cellspacing="0" style="font-family:Arial,Helvetica,sans-serif;font-size:13px;line-height:1.5;color:#2C2825"><tr><td>',
    '<div style="font-weight:bold;font-size:15px">Kevin Scrimshaw</div>',
    '<div>Family Dispute Resolution Practitioner (FDRP)</div>',
    '<div>AGD FDRP Reg. No. F2003011</div>',
    '<div><a href="https://onlinefdr.com.au" style="color:#A85C32;text-decoration:none">OnlineFDR.com.au</a> (ABN 42 961 240 633)</div>',
    '<div style="margin-top:6px">w| <a href="https://onlinefdr.com.au" style="color:#A85C32">https://onlinefdr.com.au</a></div>',
    '<div>e| <a href="mailto:hello@onlinefdr.com.au" style="color:#A85C32">hello@onlinefdr.com.au</a></div>',
    "<div>p| 1800 957 253</div>",
    '<div>f| <a href="https://www.facebook.com/onlinefdr/" style="color:#A85C32">facebook.com/onlinefdr</a></div>',
    '<div>i| <a href="https://www.instagram.com/onlinefdr.au/" style="color:#A85C32">instagram.com/onlinefdr.au</a></div>',
    "</td></tr></table>",
    "</div>",
  ].join("");
}

function leadEmailText(first) {
  return [
    "Hi " + first + ",",
    "",
    "Thanks for getting in touch. Here's what you need to know: most separations don't need to go anywhere near a courtroom, and the ones that do cost tens of thousands of dollars and drag on for a year or more.",
    "",
    "There's a better way. Family Dispute Resolution resolves most matters in weeks, for a fraction of the cost, with you and the other party keeping control of the outcome instead of handing it to a judge.",
    "",
    "See exactly what it costs: " + FEE_GUIDE_URL,
    "",
    "You pay for each stage as you reach it. No hourly billing, no surprises, and the first step, a discovery call to see if we're the right fit, is free.",
    "",
    "Book your free discovery call now: " + BOOKING_URL,
    "Or call 1800 957 253. The sooner you start, the sooner this is behind you.",
    "",
    "Kind regards,",
    "",
    "Kevin Scrimshaw",
    "Family Dispute Resolution Practitioner (FDRP)",
    "AGD FDRP Reg. No. F2003011",
    "OnlineFDR.com.au (ABN 42 961 240 633)",
    "w| https://onlinefdr.com.au",
    "e| hello@onlinefdr.com.au",
    "p| 1800 957 253",
    "f| https://www.facebook.com/onlinefdr/",
    "i| https://www.instagram.com/onlinefdr.au/",
  ].join("\n");
}

/* ---- start-lead: Google-ad funnel lead heading to booking. Alert the practice. ---- */
async function handleStartLead(data, receivedAt) {
  const name = (data.name || "").trim();
  const email = (data.email || "").trim();
  const transporter = makeTransport();

  const alertText = [
    "New /start booking lead received " + receivedAt + ".",
    "This person completed the funnel and is being sent to the booking calendar now.",
    "",
    "Name: " + (name || "Not provided"),
    "Email: " + (email || "Not provided"),
    "Phone: " + (data.phone || "Not provided"),
    "",
    "If no booking appears in your calendar shortly, follow up: they gave details but may not have finished picking a time.",
  ].join("\n");

  await transporter.sendMail({
    from: '"Online FDR Leads" <' + process.env.GMAIL_USER + ">",
    to: process.env.DESTINATION_EMAIL || process.env.GMAIL_USER,
    subject: "Start lead: " + (name || "Unnamed") + " (heading to booking)",
    text: alertText,
    replyTo: email || undefined,
  });

  console.log("Start lead handled: " + (name || "unnamed"));
  return { statusCode: 200, body: "OK" };
}

/* ---- request-a-quote: fee guide to the lead, alert to the practice ---- */
async function handleQuote(data, receivedAt) {
  const name = (data.name || "").trim();
  const first = name ? name.split(/\s+/)[0] : "there";
  const email = (data.email || "").trim();
  const matter = prettyMatter(data.matter);
  const transporter = makeTransport();

  // 1. Bold covering email to the lead (only if we have an address)
  if (email) {
    await transporter.sendMail({
      from: '"Kevin Scrimshaw, Online FDR" <' + process.env.GMAIL_USER + ">",
      to: email,
      subject: "The faster, more affordable way to resolve your separation",
      text: leadEmailText(first),
      html: leadEmailHtml(first),
    });
  }

  // 2. Alert to the practice
  const alertText = [
    "New quote request received " + receivedAt + ".",
    "",
    "Name: " + (name || "Not provided"),
    "Email: " + (email || "Not provided"),
    "Phone: " + (data.phone || "Not provided"),
    "Matter: " + (matter || "Not provided"),
    "",
    "What they need to sort out:",
    (data.description || "").trim() || "(nothing added)",
    "",
    email ? "Fee guide auto-sent to the lead." : "No email address given; fee guide NOT sent. Follow up by phone.",
  ].join("\n");

  await transporter.sendMail({
    from: '"Online FDR Leads" <' + process.env.GMAIL_USER + ">",
    to: process.env.DESTINATION_EMAIL || process.env.GMAIL_USER,
    subject: "Quote request: " + (name || "Unnamed") + (matter ? " (" + matter + ")" : ""),
    text: alertText,
    replyTo: email || undefined,
  });

  console.log("Quote handled: " + (name || "unnamed") + (email ? ", guide sent" : ", no email"));
  return { statusCode: 200, body: "OK" };
}

exports.handler = async function (event) {
  const payload = JSON.parse(event.body).payload || {};
  const data = payload.data || {};
  const form = payload.form_name;

  const receivedAt = new Intl.DateTimeFormat("en-AU", {
    dateStyle: "medium", timeStyle: "short", timeZone: "Australia/Melbourne",
  }).format(payload.created_at ? new Date(payload.created_at) : new Date()) + " (Melbourne time)";

  // Route by form. Quote requests get the fee-guide auto-reply.
  if (form === "request-a-quote") {
    return handleQuote(data, receivedAt);
  }

  // /start funnel leads heading to booking: alert the practice.
  if (form === "start-lead") {
    return handleStartLead(data, receivedAt);
  }

  // Only the intake form is handled beyond this point; ignore anything else.
  if (form && form !== "intake-safety-screen") {
    return { statusCode: 200, body: "Ignored: " + form };
  }

  const pdf = await buildPdf(data, receivedAt);

  const slug = (data.client_name || "unnamed").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  const stamp = new Date().toISOString().slice(0, 10);
  const filename = "intake-screen_" + slug + "_" + stamp + ".pdf";

  const flags = buildFlags(data);
  const subject = "Intake screen: " + (data.client_name || "Unnamed") +
    " (" + (pretty(data.matter_type) || "matter type unknown") + ")" +
    (flags.length ? " - " + flags.length + " item" + (flags.length > 1 ? "s" : "") + " flagged" : " - no flags");

  const bodyText = [
    "New intake and safety screen received " + receivedAt + ".",
    "",
    "Client: " + (data.client_name || "Not provided"),
    "Matter type: " + (pretty(data.matter_type) || "Not provided"),
    flags.length
      ? "Flagged items (" + flags.length + "):\n" + flags.map((f) => "  - " + f.q + " > " + f.a).join("\n")
      : "No safety items flagged.",
    "",
    "Full question-and-answer transcript attached as PDF.",
  ].join("\n");

  const transporter = nodemailer.createTransport({
    host: "smtp.gmail.com",
    port: 465,
    secure: true,
    auth: { user: process.env.GMAIL_USER, pass: process.env.GMAIL_APP_PASSWORD },
  });

  await transporter.sendMail({
    from: '"Online FDR Intake" <' + process.env.GMAIL_USER + ">",
    to: process.env.DESTINATION_EMAIL || process.env.GMAIL_USER,
    subject,
    text: bodyText,
    attachments: [{ filename, content: pdf, contentType: "application/pdf" }],
  });

  console.log("Intake PDF emailed: " + filename + " (" + flags.length + " flags)");
  return { statusCode: 200, body: "OK" };
};

/* Exported for local testing */
exports._internal = { buildPdf, buildFlags, SECTIONS };
