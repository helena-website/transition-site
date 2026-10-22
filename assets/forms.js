/* Intake forms for the transition site (prototype).
   Each form below mirrors a Notion database (Ideas, Event Requests, People).
   To go live: build the form in Fillout from that Notion database (see the
   "Setup: Fillout forms checklist" page in Notion), then paste the Fillout form ID
   into `fillout` below. When an ID is set, the page shows the real
   Fillout form instead of this preview, and submissions land in Notion. */
(function () {
  "use strict";

  var AGENCIES = ["Administration - DOA","Behavioral Health - BHDDH","Child Welfare - DCYF","Commerce - EOC","Corrections - DOC","Education - RIDE","Emergency Management - RIEMA","Energy - OER","Environment - DEM","Health & Human Services (Medicaid) - EOHHS","Healthcare - OHIC","Healthy Aging - OHA","Higher Education - OPC","Housing - EOH","Human Services - DHS","Office of Management and Budget - OMB","Public Health - DOH","Public Safety - DPS","Revenue - DOR","Technology - DOIT","Transportation - DOT","Utilities - PUC","Veteran Services & Affairs - VS","Workforce (Labor & Training) - DLT"];
  var GOV_OFFICE = ["Leadership (C-Suite)","Boards and Commissions","Communications","Public Engagement","Constituent Services","Legislative Affairs","Operations & Strategy","Policy","Scheduling & Administrative Support","Legal"];
  var BOARDS = ["Sample Board A","Sample Board B","Sample Commission C","Other"];
  var TOPICS = ["Health & Human Services","Education & Workforce","Economy","Housing","Public Safety & Justice","Environment & Energy","Infrastructure / Transportation","Government Operations / Budget & Technology","Other"];

  var contact = [
    { id: "name", label: "Name", type: "text", req: true, auto: "name" },
    { id: "email", label: "Email", type: "email", req: true, auto: "email" },
    { id: "phone", label: "Phone", type: "tel", req: true, auto: "tel" },
    { id: "addr", label: "Address line 1", type: "text", req: true, full: true, auto: "address-line1" },
    { id: "city", label: "City", type: "text", req: true, auto: "address-level2" },
    { id: "state", label: "State", type: "text", req: true, value: "RI", auto: "address-level1", half: true },
    { id: "zip", label: "Zip", type: "text", req: true, auto: "postal-code", pattern: "[0-9]{5}(-[0-9]{4})?" }
  ];

  var FORMS = {
    idea: {
      fillout: "cpH5hRfyCjus",
      notion: "Ideas",
      submit: "Submit idea",
      fields: [
        { id: "name", label: "Name", type: "text", req: true, auto: "name" },
        { id: "org", label: "Organization or business you represent", type: "text", full: true, hint: "Optional. Leave blank if you're writing as an individual.", auto: "organization" },
        { id: "email", label: "Email", type: "email", req: true, auto: "email" },
        { id: "city", label: "City or town", type: "text", auto: "address-level2" },
        { id: "topic", label: "Topic", type: "select", req: true, full: true, options: TOPICS },
        { id: "details", label: "Your idea", type: "textarea", req: true, full: true, hint: "What's the problem, and what would you do about it? Specifics help." },
        { id: "attach", label: "Attachment", type: "file", full: true, hint: "Optional. PDF, Word or image, up to 10 MB." }
      ]
    },
    event: {
      fillout: "",
      notion: "Event Requests",
      submit: "Send request",
      fields: [
        { sec: "About the event" },
        { id: "host", label: "Host or organization name", type: "text", req: true, full: true, auto: "organization" },
        { id: "name", label: "Event name", type: "text", req: true, full: true },
        { id: "date", label: "Event date", type: "date", req: true },
        { id: "time", label: "Event time", type: "time", req: true },
        { id: "addr", label: "Event address", type: "text", req: true, full: true },
        { id: "city", label: "City or town", type: "text", req: true },
        { id: "attend", label: "Estimated number of attendees", type: "number", min: 1 },
        { id: "purpose", label: "Event or meeting purpose", type: "textarea", req: true, full: true },
        { id: "is", label: "This event is", type: "checks", full: true, options: ["Open press event", "Open to the public"], cols: 1 },
        { sec: "Your request" },
        { id: "requesting", label: "Requesting", type: "checks", req: true, full: true, options: ["Governor-Elect", "A representative from the team"], cols: 1 },
        { id: "role", label: "Role requested", type: "checks", req: true, full: true, options: ["Speaking", "Meet and greet", "Meeting", "Attend", "Video conference"] },
        { sec: "Contact" },
        { id: "cname", label: "Contact name", type: "text", req: true, auto: "name" },
        { id: "cphone", label: "Contact phone", type: "tel", req: true, auto: "tel" },
        { id: "cemail", label: "Contact email", type: "email", req: true, full: true, auto: "email" },
        { id: "attach", label: "Attachments", type: "file", full: true, multiple: true, hint: "Optional. Agenda, flyer or run of show." },
        { id: "more", label: "Anything else we should know?", type: "textarea", full: true }
      ]
    },
    boards: {
      fillout: "",
      notion: "People (Track: Board or Commission)",
      submit: "Submit interest",
      fields: [{ sec: "Contact information" }].concat(contact, [
        { sec: "Boards and commissions" },
        { id: "boards", label: "Which boards or commissions interest you?", type: "checks", req: true, full: true, options: BOARDS, hint: "Sample list. The final list of Tier 1 and Tier 2 appointments is still being set." },
        { sec: "Résumé" },
        { id: "resume", label: "Résumé (PDF)", type: "file", req: true, full: true, accept: ".pdf" },
        { id: "comments", label: "Additional comments", type: "textarea", full: true, hint: "Relevant experience, community ties, or anything else that helps the team." }
      ])
    },
    serve: {
      fillout: "",
      notion: "People (Track: Administration)",
      submit: "Submit interest",
      fields: [{ sec: "Contact information" }].concat(contact, [
        { sec: "Where you'd like to work" },
        { id: "agencies", label: "Rhode Island state agencies", type: "checks", full: true, options: AGENCIES, hint: "Check any that apply." },
        { id: "gov", label: "Governor's Office", type: "checks", full: true, options: GOV_OFFICE },
        { sec: "Documents" },
        { id: "cover", label: "Cover letter (PDF)", type: "file", req: true, accept: ".pdf" },
        { id: "resume", label: "Résumé (PDF)", type: "file", req: true, accept: ".pdf" },
        { id: "comments", label: "Additional comments", type: "textarea", full: true }
      ]),
      oneOf: ["agencies", "gov"]
    }
  };

  function el(tag, attrs, kids) {
    var n = document.createElement(tag);
    for (var k in attrs || {}) {
      if (attrs[k] === true) n.setAttribute(k, "");
      else if (attrs[k] !== false && attrs[k] != null) n.setAttribute(k, attrs[k]);
    }
    (kids || []).forEach(function (c) { n.append(c); });
    return n;
  }

  function field(key, f) {
    if (f.sec) return el("h3", { class: "fsec" }, [f.sec]);
    var id = key + "-" + f.id;
    var cls = "field" + (f.full || f.type === "checks" ? " full" : "");
    var labelKids = [f.label];
    if (f.req) labelKids.push(el("span", { class: "req", "aria-hidden": "true" }, ["*"]));
    var hint = f.hint ? el("p", { class: "hint", id: id + "-hint" }, [f.hint]) : null;
    var describedBy = f.hint ? id + "-hint" : null;

    if (f.type === "checks") {
      var box = el("div", { class: "checks" + (f.cols === 1 ? " one" : "") });
      f.options.forEach(function (o, i) {
        box.append(el("label", {}, [el("input", { type: "checkbox", name: f.id, value: o, id: id + "-" + i }), o]));
      });
      var fs = el("fieldset", { class: cls, "data-req": f.req ? "1" : null, "data-name": f.id, "aria-describedby": describedBy }, [el("legend", {}, labelKids)]);
      if (hint) fs.append(hint);
      fs.append(box);
      return fs;
    }

    var input;
    var common = { id: id, name: f.id, required: !!f.req, autocomplete: f.auto || null, "aria-describedby": describedBy };
    if (f.type === "textarea") input = el("textarea", common);
    else if (f.type === "select") {
      input = el("select", common, [el("option", { value: "" }, ["Choose a topic"])]);
      f.options.forEach(function (o) { input.append(el("option", { value: o }, [o])); });
    } else {
      common.type = f.type;
      if (f.value) common.value = f.value;
      if (f.pattern) common.pattern = f.pattern;
      if (f.min != null) common.min = f.min;
      if (f.accept) common.accept = f.accept;
      if (f.multiple) common.multiple = true;
      if (f.type === "tel") common.inputmode = "tel";
      if (f.id === "zip") common.inputmode = "numeric";
      input = el("input", common);
    }
    var wrap = el("div", { class: cls }, [el("label", { for: id }, labelKids)]);
    if (hint) wrap.append(hint);
    wrap.append(input);
    return wrap;
  }

  function render(slot) {
    var key = slot.getAttribute("data-form");
    var cfg = FORMS[key];
    if (!cfg) return;

    if (cfg.fillout) {
      slot.innerHTML = "";
      slot.append(el("div", { class: "fillout-slot", style: "width:100%;height:900px", "data-fillout-id": cfg.fillout, "data-fillout-embed-type": "standard", "data-fillout-inherit-parameters": true, "data-fillout-dynamic-resize": true }));
      var s = document.createElement("script");
      s.src = "https://server.fillout.com/embed/v1/";
      document.body.append(s);
      return;
    }

    var form = el("form", { class: "intake", novalidate: true, "aria-label": slot.getAttribute("data-label") || "Form" });
    var grid = el("div", { class: "fgroup" });
    cfg.fields.forEach(function (f) { grid.append(field(key, f)); });
    form.append(grid);
    var msg = el("div", { class: "form-msg", role: "status", "aria-live": "polite", hidden: true });
    form.append(el("div", { class: "form-foot" }, [
      el("p", { class: "hint" }, ["Fields marked ", el("span", { class: "req" }, ["*"]), " are required."]),
      el("button", { class: "btn btn-green", type: "submit", style: "justify-self:start" }, [cfg.submit]),
      msg
    ]));

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var problems = [];
      Array.prototype.forEach.call(form.querySelectorAll("input,select,textarea"), function (i) {
        if (i.type !== "checkbox" && !i.checkValidity()) problems.push(i);
      });
      Array.prototype.forEach.call(form.querySelectorAll("fieldset[data-req]"), function (fs) {
        if (!fs.querySelector("input:checked")) problems.push(fs.querySelector("input"));
      });
      if (cfg.oneOf) {
        var any = cfg.oneOf.some(function (n) { return form.querySelector('input[name="' + n + '"]:checked'); });
        if (!any) problems.push(form.querySelector('input[name="' + cfg.oneOf[0] + '"]'));
      }
      msg.hidden = false;
      if (problems.length) {
        msg.className = "form-msg bad";
        msg.textContent = cfg.oneOf && problems.length === 1 && problems[0].name === cfg.oneOf[0]
          ? "Choose at least one agency or Governor's Office area."
          : "Please fill in the required fields (" + problems.length + " missing or invalid).";
        problems[0].focus();
        return;
      }
      msg.className = "form-msg ok";
      msg.textContent = "Prototype: this is a preview, so nothing was sent. In the live version this goes to the " + cfg.notion + " database in Notion.";
    });

    slot.innerHTML = "";
    slot.append(form);
  }

  document.querySelectorAll("[data-form]").forEach(render);
})();
