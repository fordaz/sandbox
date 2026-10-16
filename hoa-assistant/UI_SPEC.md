# HOA CC&R Assistant: Manager UI Specification

Status: v1 draft, derived from the clickable prototype (`prototype/Inbox.dc.html`).
Scope: the **property manager's** web experience only. Back end, ingestion, AI and
channel integrations are out of scope here; where the UI depends on them, the
expected data is described in [§10 Front-end data model](#10-front-end-data-model).

---

## 1. Product summary

Residents send questions about their community's governing documents (CC&Rs,
Rules & Regulations, Bylaws, phase supplements) by **email** or **WhatsApp**.
Each question becomes a **case**. The assistant answers it using only those
documents and pre-writes a reply. The manager:

1. sees all cases in a **Queue**,
2. opens one into the **Answer** screen,
3. checks the answer against the highlighted source clauses,
4. asks the assistant more questions in the same conversation if needed,
5. adds grounded answers to the draft, edits it, and
6. sends the reply on the resident's original channel.

The manager can also start **internal questions** (no resident involved) from
the Queue. These use the same Answer screen without a draft.

Core principle: **every statement that reaches a resident is traceable to a
clause on a page**, and the source is always visible next to the text.

---

## 2. Glossary

| Term | Meaning |
|---|---|
| **Case** | One inbound resident conversation (email thread or WhatsApp chat) or one internal question. The unit shown as a row in the Queue. |
| **Channel** | `email`, `whatsapp`, or `internal`. |
| **Resident match** | The resident record (name, lot, phase, contact) matched from the sender's email or phone number. |
| **Document** | An indexed governing document (PDF), e.g. "CC&Rs". |
| **Clause** | A numbered section of a document (e.g. `§D.3`, `R-6.2`) with a page number and highlight rectangles. |
| **Citation** | A reference from an answer or the draft to a clause. Numbered per case: `[1]`, `[2]`, … |
| **Assistant answer** | An assistant message in the case conversation. Either **grounded** (has ≥1 citation) or **not grounded** ("Not in your documents"). |
| **Draft** | The reply being prepared for the resident. Made of paragraphs that may contain citations. |
| **Include in draft** | Action on a grounded assistant answer that adds its resident-facing version to the draft. |
| **Holding reply** | A draft for a question the documents don't answer. It acknowledges the question without stating a rule. |

---

## 3. Information architecture and routes

```
/inbox                         Queue (default filter = all)
/inbox?filter=review|notfound|mine|sent&q=<search>
/cases/:caseId                 Answer screen for a case
/cases/new                     Answer screen for a new internal question (creates case on first ask)
/documents                     (placeholder nav item; out of scope for v1)
```

- The Answer screen keeps the Queue's filter and search in its URL or state, so
  **Previous / Next** step through the same list the manager came from.
- Deep links to a citation are optional for v1:
  `/cases/:caseId?cite=2` opens the case with citation 2 active.

---

## 4. Visual language (design tokens)

These are the values used in the prototype. Implement them as CSS variables or theme tokens.

### 4.1 Color

| Token | Value | Use |
|---|---|---|
| `--ink` | `#18212B` | Primary text, app header background, dark buttons, selected filter tab |
| `--ink-2` | `#3F4852` | Secondary text |
| `--muted` | `#4A545E` | Labels, meta text (≥4.5:1 on white and on `--bg`) |
| `--line` | `#E1E4E8` | Panel borders |
| `--line-2` | `#CDD3D9` | Control borders |
| `--bg` | `#F3F4F6` | App background |
| `--bg-2` | `#FAFBFC` | Conversation background |
| `--viewer-bg` | `#E4E7EA` | Document viewer canvas |
| `--surface` | `#FFFFFF` | Cards, panels, pages |
| `--accent` | `#2147C4` | Primary buttons, focus ring, links |
| `--accent-hover` | `#1B3BA8` | |
| `--accent-soft` | `#E6ECFB` / `#EEF2FD` | Focus halo, citation chip background |
| `--hl` | `#FFF3B0` | Cited clause highlight (inactive) |
| `--hl-active` | `#FFE14D` | Active cited clause, active citation chip |
| `--hl-ring` | `#D9A900` | Active clause outline |
| Status green | bg `#E3F2E9` / fg `#1A5E37` | Sent, ✓ checks, WhatsApp channel tint |
| Status blue | bg `#E6ECFB` / fg `#1B3BA8` | Draft ready, email channel tint |
| Status amber | bg `#FFEFC7` / fg `#6E4600` | Not in documents, citation warnings |
| Status gray | bg `#ECEEF0` / fg `#3F4852` | Draft saved, holding reply |
| Status purple | bg `#F0EAFB` / fg `#5B3A9E` | Internal / My question |
| Status red | bg `#FDE7E4` / fg `#9B2C1F` | Urgent, reply window < 8h |

Yellow is reserved for **source grounding** (highlights and active citations).
Don't use it for anything else.

### 4.2 Typography

- UI: **IBM Plex Sans** 400/500/600. Base 14px; meta 12px; labels 11px
  uppercase with 0.06em letter spacing; page title 26px/600; case name 15px/600.
- Document pages: **Source Serif 4** 400/600, 15px, line-height 1.7, justified.
- Use tabular numerals for page counters and counts.

### 4.3 Shape, spacing, motion

- Radii: 6px (controls), 8px (buttons, inputs), 10–12px (cards, panels), 999px (pills, chips).
- Spacing scale: 4, 6, 8, 10, 12, 14, 16, 20, 24, 32.
- Page shadow: `0 1px 3px rgba(16,24,40,.12), 0 10px 28px rgba(16,24,40,.08)`.
- Motion:
  - clause highlight fades in over 500ms; the active clause gets a single 1.6s outward "pulse" ring
  - a newly included draft paragraph flashes `--hl` and fades out over about 2.5s
  - viewer and chat scroll smoothly
- Respect `prefers-reduced-motion` by turning off the pulse, flash and smooth scrolling.

### 4.4 Icons

Use simple line icons (1.4–1.8px stroke) for:

| Name | Use |
|---|---|
| `chat-bubble` | WhatsApp |
| `envelope` | Email |
| `lock` | Internal / private |
| `clock` | Reply window |
| `pin` | Pinned message |
| `check` | Confirmations |
| `plus` | New question, Include in draft |
| `pencil` | Edit |
| `chevron-left/right` | Navigation |
| `arrow-up` | Send question |
| `arrow-right` | Reply |
| `shield` | Assistant avatar |

Don't use third-party brand logos in the product UI. Show the channel as an icon plus a text label.

---

## 5. Global shell

### 5.1 App header (all screens)

Height 56px, background `--ink`, white text. Left to right:

1. **Logo + product name** ("CC&R Assistant").
2. Vertical divider.
3. **Primary nav**:
   - `Inbox` with a yellow count badge showing open cases (not internal, not sent). Selected state: background `#2A3542`.
   - `Documents` (placeholder).
4. Flexible spacer.
5. **Community and index status**: green dot, then "Willow Creek Estates HOA · 4 documents · 86 pages indexed".
   - v1 later: this becomes a community switcher for managers of several HOAs.
6. **Avatar** with the manager's initials. Clicking it opens the account menu (out of scope).

### 5.2 Global toast

- Bottom center, dark (`--ink`), with a green check, auto-dismissing after 3.2s.
- Uses `role="status"`.
- Shown for "Draft saved", "Reply sent to {name} on WhatsApp. Opened the next message.", and "Inbox is clear."

---

## 6. Screen 1: Queue (`/inbox`)

### 6.1 Layout

A scrollable page with 28px/32px padding and content `max-width: 1320px`, centered.

```
┌ App header ─────────────────────────────────────────────────────────────────────────┐
│ Inbox                                          [ Search name, lot or message ] [+ New question] │
│ 6 waiting for a reply · 1 sent today                                                │
│ [All 7] [Needs reply 6] [Not in documents 1] [My questions 1] [Sent 0]              │
│ ┌───────────────────────────────────────────────────────────────────────────────┐   │
│ │ FROM            MESSAGE                     STATUS        SOURCES  RECEIVED  REPLY WINDOW │
│ │ ● 💬 Ken Ito    Hi, the house at 24 has…    Draft ready   2 clauses 11:40 PM  14h left   │
│ │   Lot 22·Ph 1                               Urgent                 Yesterday             │
│ │ ...                                                                              │   │
│ └───────────────────────────────────────────────────────────────────────────────┘   │
│ Connected: Email · management@… · WhatsApp Business · … · Residents matched by …    │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Components

**PageTitle**
- H1 "Inbox".
- Summary line: `{open} waiting for a reply · {sentToday} sent today`.

**SearchInput** (`type="search"`, 260px)
- Filters rows client-side, case-insensitively, on resident name, lot, subject and message text. (Server-side search in the full version.)
- Updates the URL `q`, debounced by 200ms.

**NewQuestionButton** (primary)
- Opens `/cases/new`. See [Flow F8](#f8-new-internal-question).

**FilterTabs** (`role="tablist"`)
- Each tab shows its label and count. The selected tab is dark (`--ink`) with white text.

| Filter | Shows |
|---|---|
| All | every case |
| Needs reply | not internal and not sent |
| Not in documents | `notFound` and not sent |
| My questions | internal cases |
| Sent | not internal and sent |

**CaseTable**
- A white card with a 12px radius and a header row. Column labels are uppercase 11px on `#F7F8F9`.
- Columns: `minmax(210px,1.25fr) | minmax(260px,2.6fr) | 180px | 100px | 120px | 110px`.
- Below 1000px of content width the table scrolls horizontally inside the card.

**CaseRow**
- One `<button>` (or row link) per case, full width, at least 72px tall.
- Hover background `#F5F7FB`. Activating the row opens `/cases/:id`.

| Column | Content |
|---|---|
| **From** | Unread dot (8px, `--accent`; hidden when read or internal), **ChannelBadge** (34px rounded square: WhatsApp green tint + chat icon, Email blue tint + envelope, Internal purple tint + lock; has an `aria-label`), resident name (bold when unread, ellipsis), and below it `Lot {lot} · Phase {phase}` or `Internal · only you` |
| **Message** | Email subject (600 weight, one line, ellipsis) if any, then the message snippet clamped to 2 lines; newlines collapsed |
| **Status** | **StatusPill** (see [§11](#11-case-statuses)) plus an optional red `Urgent` pill |
| **Sources** | `{n} clause(s)` cited so far, or `—` |
| **Received** | Time (e.g. `11:40 PM`) and relative time below (`Yesterday`, `12 min ago`) |
| **Reply window** | WhatsApp only: `{h}h left`, shown red and bold when under 8h; `Replied` after sending; `—` for email and internal |

**Default sort**
1. Urgent first.
2. Then by WhatsApp reply window, soonest first.
3. Then oldest received first.

Sent cases sink to the bottom in the All filter.

**EmptyState** (no rows match)
- "Nothing here. Every message in this view has been handled."

**ChannelFooter** (12px, `--muted`)
- Connected email address, WhatsApp Business number, and "Residents matched by email or phone against the resident roster".

### 6.3 Queue states

| State | Behaviour |
|---|---|
| Loading | 6 skeleton rows at the same height as real rows |
| Error | Inline banner above the table with Retry |
| Live update | When a new case arrives: prepend it with a 1s soft highlight, update counts and the header badge. Never reorder rows under the pointer; if the user is hovering, show a "1 new message · Show" pill instead |
| Unread | Opening a case marks it read |

---

## 7. Screen 2: Answer (`/cases/:id`)

### 7.1 Layout

```
┌ App header ──────────────────────────────────────────────────────────────────────────────────────┐
├ CaseHeader: [← Inbox] [‹] 3 of 7 [›] │ (ch) Dan Kim                         [Draft ready] ⏱ 23h left…│
│                                         Lot 117 · Phase 2 · WhatsApp +1… · matched to roster          │
├──────────────────────────────── DocumentViewer ──────────┬──────── RightPane (540px) ──────────────┤
│ [CC&Rs][Rules][Phase 2 Supp.●][Bylaws]     ‹ Page 3 of 6 ›│ DraftPanel (resizable height)          │
│ Cited in this case: [1 §D.3 · Phase 2 Supp. p.3] [2 …]   │  DRAFT REPLY  [WhatsApp]   Undo  [Edit] │
│ ┌──────────────────────── page ──────────────────────┐   │  Hi Dan, thanks for reaching out!       │
│ │  ① ████ §D.3 Restricted Breeds … ████             │   │  Lot 117 is in Phase 2 … [1] … [2]     │
│ │  ② ▒▒▒▒ §D.4 Existing Animals … ▒▒▒▒              │   │  ✓ Every statement cited  Friendly|Formal  [Save] [Reply on WhatsApp →] │
│ └─────────────────────────────────────────────────────┘   ├══════════ Splitter ═════════════════════┤
│                                                           │ ConversationPanel                        │
│                                                           │  CASE CONVERSATION   🔒 Only you can see  │
│                                                           │  📌 Dan: Hi! Is it ok if we get a pit…   │
│                                                           │  [resident msg] [assistant card] [you] … │
│                                                           │  Suggested: (What if…) (Does Lot 117…)   │
│                                                           │  [ Ask about this case…            ↑ ]   │
└───────────────────────────────────────────────────────────┴─────────────────────────────────────────┘
```

- The whole screen fills the viewport height (`100vh` minus the header). The page itself doesn't scroll; each panel scrolls on its own.
- Left: **DocumentViewer**, `flex: 1 1 auto; min-width: 0`.
- Right: **RightPane**, fixed at 540px (configurable 480–600px), white, a column of **DraftPanel**, then **Splitter**, then **ConversationPanel**.
- Internal cases have no DraftPanel and no Splitter, so the ConversationPanel fills the right pane.

### 7.2 CaseHeader

A white bar, at least 56px tall, with a bottom border. It wraps on narrow widths.

1. **Back button** (`← Inbox`, ghost, small). Returns to `/inbox` with the same filter and search.
2. **CaseNavigator**: previous and next icon buttons around the label `{i} of {n}`, for the current Queue list. Buttons are disabled at the ends.
   - Previous/next follows the Queue list as it was when the screen opened, so it doesn't jump around when statuses change.
3. Divider.
4. **ChannelBadge**, **resident name** (15px/600), and below it, the detail line:
   - Resident: `Lot {lot} · Phase {phase} · {WhatsApp|Email} {contact} · matched to resident roster`
   - Internal: `Internal question · not sent to anyone`
   - Unmatched sender: `Unmatched sender · {contact}` with a **Match resident…** link (opens a roster search popover; out of scope for v1 visuals).
5. Spacer.
6. **StatusPill**.
7. **ReplyWindow** (WhatsApp only, before sending): clock icon and `{h}h left to reply on WhatsApp`, red under 8h. Under 1h it also shows a red banner in the DraftPanel (see [F11](#f11-whatsapp-reply-window-expired)).

### 7.3 DocumentViewer

Built on a PDF renderer with a text layer and a highlight overlay. Sub-components:

**DocTabs**
- One tab per indexed document, in a fixed order (CC&Rs, Rules & Regulations, Phase 2 Supplement, Bylaws).
- A small amber dot appears after the name if any citation in the current case points into that document.
- The selected tab has a 2px `--ink` underline.
- Clicking a tab opens that document at its first page, or at the first cited page if the document has citations in this case.

**PageNav**
- Previous and next icon buttons with `Page {n} of {total}`.
- v1 extras (optional): zoom (fit-width / 100% / 125%), download PDF, a page-number input.

**CitationStrip** (directly under the tabs, `#F7F8F9`)
- With citations: the label "Cited in this case", then one chip per case citation, in order: `[n] {clause} · {doc short} p. {page}`.
- The active chip is yellow (`--hl-active`). Clicking a chip activates that citation (see [F2](#f2-activate-a-citation)).
- Without citations: "No clause cited yet. Ask a question and the clause behind each answer is highlighted here."

**PdfPage + HighlightLayer**
- Renders the current page centered, max width about 780px, as a white sheet with a shadow on the `--viewer-bg` canvas.
- For every case citation on the visible page, draw its rectangles:
  - inactive citation: fill `--hl`
  - active citation: fill `--hl-active`, 2px `--hl-ring` outline, and a single pulse
- **MarginMarker**: a 24px dark circle with the citation number, placed in the left margin next to the first rectangle of each cited clause.
- Clicking a highlighted clause activates that citation.
- When a citation is activated, scroll the page so the clause's top sits about one third down the viewport (smooth scroll).
- Continuous-scroll mode (all pages stacked) is acceptable as long as activation scrolls to the right page and position.

**Viewer states**
- **Loading:** a page skeleton.
- **Failed to load:** "Couldn't load this document" with Retry. The citations stay listed in the strip.
- **Clause rectangles missing** (ingestion gap): jump to the page, show the clause text in a callout above the page, and log an error.

### 7.4 DraftPanel (resident cases only)

A fixed-height region whose height is controlled by the Splitter. Default 340px, min 170px, max 620px (or 70% of the right pane). The height is remembered per user.

**Header row**
- Label `DRAFT REPLY` (`SENT REPLY` after sending), then a channel pill (`WhatsApp` green or `Email` blue).
- Spacer.
- After an include: an "Added to draft" note and an **Undo** link, until the next draft change.
- **Edit / Done** toggle (ghost, small, `aria-pressed`). Hidden once sent.

**EmailMeta** (email only)
- `To: {name} <{email}>`
- `Subject: Re: {original subject}`. The subject is editable in edit mode.

**Body** (scrolls)
- **View mode:** a list of paragraphs (`white-space: pre-line`, line-height 1.6). Citation markers render as **CitationChips**: small blue-tinted buttons with the number. Hovering or activating a chip activates that citation in the viewer.
  - A newly included paragraph flashes yellow (see §4.3).
  - A holding-reply paragraph uses `--ink-2`.
- **Edit mode:** a rich-text editor in which citations are **atomic inline tokens** (chips that can't be partly edited and can be deleted as a whole).
  - Recommended: TipTap/ProseMirror with a `citation` node holding `{n}`.
  - The prototype falls back to a plain textarea with `[n]` markers; the real version must not lose the citation links when edited.
  - Paragraph breaks are real blocks.
  - The greeting and sign-off are ordinary editable paragraphs.

**Footer row**
- **CitationCheck pill** (left), worked out live from the draft's body paragraphs (all paragraphs except the greeting and sign-off):

  | Condition | Pill |
  |---|---|
  | Every body paragraph has ≥1 citation (holding paragraphs exempt) | green `✓ Every statement cited` |
  | Any non-holding body paragraph without a citation | amber `{n} paragraph(s) have no citation` (clicking scrolls to the first offender and outlines it) |
  | Only holding paragraphs | gray `Holding reply · no rule stated` |
  | Sent | green `Sent {time} · logged with citations` |

  Future: check per sentence instead of per paragraph.
- Spacer.
- **ToneToggle**: segmented `Friendly | Formal`. Switching regenerates the greeting and sign-off only. It's disabled (with a tooltip "Tone is fixed after manual edits") once the draft has been edited by hand.
  - Future: AI tone rewrite of the whole body, with a diff preview.
- **Save** (ghost): saves the draft, sets status `Draft saved`, toast "Draft saved".
- **Reply** (primary): label `Reply on WhatsApp` or `Send email`, with an arrow icon. See [F6](#f6-reply-send).

The footer is hidden once sent. After sending, the panel shows the sent text read-only, with the green Sent pill.

**Channel-specific drafting rules** (for the generated text, shown here for the UI copy)

| | WhatsApp | Email |
|---|---|---|
| Friendly greeting | `Hi {first}, thanks for reaching out!` | `Hi {first},` |
| Friendly sign-off | `Let me know if anything else comes up.\n– {Management name}` | `Thanks, and let me know if anything else comes up.\n{Management name}` |
| Formal greeting | `Hello {first},` | `Dear {full name},` |
| Formal sign-off | `Regards,\n{HOA} Management` | `Sincerely,\n{HOA} Management` |
| Length guidance | 1–3 short paragraphs, plain text | Paragraphs |
| How citations go out | Inline short refs, e.g. "(Phase 2 Supplement §D.3)", plus an optional link to the cited page | Footnotes list "Sources: [1] Phase 2 Supplement §D.3, p. 3 …"; optional "Attach cited pages (PDF)" checkbox in a future version |

The UI always shows numbered chips. Converting them to the outbound format happens on send. Show a **Preview as resident** link (future) that renders the outbound version.

### 7.5 Splitter

- A 14px-tall full-width bar with a centered 44×4 grip, on `#F3F4F6`, using `cursor: row-resize`.
- It's a focusable button with `aria-label="Resize draft. Drag, or use the up and down arrow keys"`.
- Pointer drag uses pointer capture. The keyboard arrow keys resize in 24px steps. Double-click resets to the default height.

### 7.6 ConversationPanel

**Header**
- Label `CASE CONVERSATION` (internal: `YOUR QUESTION`).
- On the right, a lock icon and "Only you can see this conversation".

**PinnedResidentMessage** (resident cases)
- A one-line strip on `--bg-2`: pin icon, `**{first}:** {message}`, truncated.
- It's a button with `aria-expanded`. Clicking it expands to the full text with newlines kept.
- If the resident sends more messages, it shows the latest one with `+{n} more`.

**MessageList** (scrolls, 14px gap, `--bg-2` background)
- Auto-scrolls to the bottom when the case opens and when a message is added, unless the user has scrolled up. In that case show a "New message ↓" pill instead.
- Message item types:

| Type | Look |
|---|---|
| **ResidentWhatsAppMessage** | Left-aligned, max 88% wide. Meta line `{name} · WhatsApp · {time}`. Bubble `#E3F2E9`, radius `4 12 12 12`, pre-line text. Media attachments (future): thumbnails |
| **ResidentEmailMessage** | Left-aligned card, 92% wide, white with a border. Header strip `#F3F5FA` with `**{name}** · Email · {time}` and `Subject: …`. Body pre-line. Quoted history collapsed behind "Show quoted text" |
| **ManagerMessage** | Right-aligned, max 82% wide. Meta `You`. Dark bubble (`--ink`), white text, radius `12 4 12 12` |
| **AssistantCard** | Full-width card, white, border, 12px radius. Details below |
| **ThinkingIndicator** | A card with three animated dots and "Searching 4 documents · 86 pages", with `role="status"`. Shown while an answer is pending |
| **SystemEvent** (future) | A centered 12px muted line, e.g. "Reply sent by Alex · 9:26 AM", "Draft saved", "Assigned to Board" |

**AssistantCard** contents
1. **Header:** shield avatar (22px, yellow tint), then "Assistant", then a meta line: `Grounded in {n} clause(s)` or `No matching clause`.
2. **Body:** the answer text (line-height 1.55) with inline **CitationChips**, numbered per case.
3. **SourceChips** (grounded only): one chip per distinct citation, `[n] {clause} · {doc} p. {page}`. Clicking activates the citation.
4. **Action row:**
   - Grounded, has a resident-facing version, not yet in the draft, and the case isn't sent: **Include in draft** (outline accent button with a plus icon).
   - Already in the draft: a green `✓ In draft` tag. v1 behaviour: not clickable; use Undo or edit the draft. Optional: clicking removes that paragraph, with a confirmation.
   - Not grounded: an amber `Not in your documents` pill and the note "Can't be added to the draft".
   - Internal cases: no include action. Future: "Turn into announcement".
   - Always (future): Copy, plus a 👍/👎 feedback icon pair.

**SuggestedQuestions** (above the composer)
- The label "Suggested", then 1–3 dashed outline chips with case-specific follow-up questions.
- Clicking one asks it immediately. A chip disappears once asked. All chips are disabled while an answer is pending.

**Composer**
- A form with a hidden label: a single-line input (multi-line, growing up to 4 lines, in the full version) and a square send button with an up-arrow icon.
- Placeholder: `Ask about this case…` (internal: `Ask the governing documents…`).
- Enter sends; Shift+Enter adds a newline. Send is disabled while the input is empty or an answer is pending.
- The input clears on send and keeps focus.

**Empty conversation** (new internal question)
- Centered content:
  - Title "Ask the governing documents".
  - Text "Your question and its answer stay private and are saved under My questions. Every answer links to the clause it came from."
  - Starter chips: "Can I install solar panels on my roof?", "What are the weekend guest parking rules?", "How do I report a noise complaint after 10 PM?", "Are aggressive dog breeds restricted?"

---

## 8. Flows

### F1. Open a case from the Queue
1. Click a row. Go to `/cases/:id` and mark the case read.
2. Viewer: if the case has citations, open the first one's document and page, make citation 1 active, and scroll to it. Otherwise show CC&Rs page 1 (or the table of contents).
3. Conversation scrolls to the bottom (latest message).
4. Draft shows the AI-generated draft. The first grounded answer is already marked ✓ In draft.

### F2. Activate a citation
Triggered by a click on any CitationChip (draft, assistant card, source chip, citation strip) or a highlighted clause in the viewer.
1. Set `activeCitation = n` for the case.
2. The viewer switches document and page if needed and scrolls the clause into view (about one third from the top).
3. The clause gets the active highlight and pulses once. Every chip with that number turns yellow in all panels.
4. No state change on the draft or the conversation.

### F3. Ask a question (manager)
1. The manager types or clicks a suggestion, then submits.
2. Append a ManagerMessage at once (optimistic). Show the ThinkingIndicator. Disable the composer's send button and the suggestion chips.
3. The answer arrives. Replace the indicator with an AssistantCard.
   - New clauses get the next citation numbers for the case. Reused clauses keep their existing numbers.
4. If the answer is grounded, activate its first citation (F2).
5. On error: show an inline error card "Couldn't get an answer. Retry" in place of the indicator. The manager message stays.
6. The question is understood in the context of the case: resident, lot, phase, the original message and earlier turns.

### F4. Include in draft
1. Click **Include in draft** on an AssistantCard.
2. Save an undo snapshot of the draft.
3. Add the answer's resident-facing paragraph to the draft:
   - Untouched draft: append it after the last body paragraph and before the sign-off.
   - Manually edited draft: insert it before the last paragraph (assumed to be the sign-off).
   - Full version: the back end may instead return a rewritten whole draft that merges the new content. The UI then shows a diff highlight on the changed paragraphs.
4. Citations keep their case numbers.
5. Flash the new paragraph, scroll the draft to it, and show "Added to draft · Undo" in the header. The card's button becomes ✓ In draft.
6. If the draft was in edit mode, leave edit mode first (after committing the edits) or insert at the cursor. The prototype leaves edit mode.

### F5. Undo the last include
Restore the snapshot (body paragraphs and the set of included answers) and hide the Undo link. One level of undo is enough for v1. The editor's own undo covers manual typing.

### F6. Reply (send)
1. Click **Reply on WhatsApp** or **Send email**.
2. Pre-send checks. Any of these opens a **confirm dialog** listing the issues, with "Send anyway" and "Go back":
   - The citation check isn't green (uncited paragraphs).
   - The WhatsApp window has expired (see F11).
   - The draft is empty or only greeting and sign-off.
3. Sending: the button shows a spinner and the draft is locked.
4. Success:
   - Mark the case Sent with the time.
   - The draft becomes read-only "Sent reply".
   - A SystemEvent is added to the conversation.
   - **Auto-advance** to the next unsent resident case in the Queue's order, with the toast "Reply sent to {name} on WhatsApp. Opened the next message."
   - If none remain, go to `/inbox` with the toast "{…}. Inbox is clear."
5. Failure: an error banner in the DraftPanel ("Couldn't send. {reason}. Retry"). The draft stays editable.

A setting (future) controls auto-advance: on (default) or return to Queue.

### F7. Save
Persist the draft (manual Save; also autosave every 5s while it changes, as a quiet status "Saved · 9:24"). Status becomes `Draft saved` if it was `Draft ready` or `Not in documents`. Toast "Draft saved" on manual save only.

### F8. New internal question
1. Click **+ New question** on the Queue. Go to `/cases/new`: no draft, empty conversation with starter chips.
2. On the first question, create the case (channel `internal`, status `My question`). Its title is the question, truncated to 48 characters. Replace the URL with `/cases/:id`.
3. It appears under **My questions** and **All**.
4. A case with no questions asked is thrown away when the manager leaves.

### F9. Not-in-documents case (holding reply)
- The initial assistant answer is not grounded, so the case shows `Not in documents` in the Queue.
- The draft starts as a **holding reply**: an acknowledgement and a promise to follow up, with `[DATE]` placeholders highlighted for the manager to fill.
- The manager can ask related questions. Grounded answers can be included, for example "The Board meets at least quarterly [1]…", which turns the citation check green.
- Placeholders still in the draft (`[...]`) block sending, with the confirm dialog's issue "Fill in placeholders".

### F10. Resident sends another message while the case is open or unsent
- The new message is appended to the conversation (live) and the pinned strip updates.
- The assistant answers it automatically (ThinkingIndicator, then an AssistantCard). The answer is **not** auto-included; its Include button is prominent.
- A banner in the DraftPanel says "Dan sent a new message · Review" (scrolls to it).
- In the Queue, the case's status goes back to `Draft ready` (or `Needs review`) and it shows as unread.
- If the case was already Sent, it reopens as a new reply round. The previous sent reply stays as a SystemEvent with the text.

### F11. WhatsApp reply window expired
- At 0h, the ReplyWindow turns red with "Reply window closed".
- The DraftPanel shows a banner: "WhatsApp only allows template messages after 24 hours. Send as template?" The Reply button becomes **Send template…**, which opens a picker of pre-approved templates (future) with the draft summary as a variable. Alternatives: **Send by email** if an email address is on file, or **Mark as handled**.

### F12. Navigate between cases
- **‹ / ›** or the keyboard shortcuts (§12) move through the Queue list.
- If the draft has unsaved edits, autosave first. There's never a blocking "discard changes?" prompt in v1, because autosave makes it unnecessary.

### F13. Edit the draft by hand
- Edit lets the manager change any text. Citation chips stay atomic.
- Deleting all chips from a paragraph turns the citation check amber.
- Typing new factual text isn't detected in v1, except by the per-paragraph rule.
- Done returns to view mode. The tone toggle is then disabled (see §7.4).

### F14. Other case actions (v1.1, not in the prototype)
These live in an overflow menu `⋯` in the CaseHeader:
- **Assign to…** a teammate or the Board. Status `Assigned`.
- **Escalate** (needs a Board decision): requires a note. Status `Escalated`.
- **No reply needed**: closes the case. Status `Closed`.
- **Mark unread.**

---

## 9. Citation numbering rules

- Numbering is **per case**, starting at 1, in order of first appearance across all assistant answers in the case.
- The same clause always keeps the same number within a case. A later answer that cites `§D.3` again reuses `[1]`.
- Draft chips, assistant chips, source chips, the citation strip and the margin markers all use the same number.
- The citation strip lists all case citations, including ones not in the draft. Future: dim citations not used in the draft.

---

## 10. Front-end data model

TypeScript shapes the UI expects. Field names are suggestions.

```ts
type Channel = 'email' | 'whatsapp' | 'internal';

type CaseStatus =
  | 'draft_ready' | 'needs_review' | 'not_found' | 'draft_saved'
  | 'sent' | 'my_question' | 'assigned' | 'escalated' | 'closed';

interface ResidentMatch {
  residentId: string;
  name: string;            // "Dan Kim"
  firstName: string;       // "Dan"
  lot: string;             // "117"
  phase: string;           // "2"
  contact: string;         // "+1 555-0117" | "dan@example.com"
  matchedBy: 'phone' | 'email' | 'manual';
}

interface CaseSummary {          // Queue row
  id: string;
  channel: Channel;
  title: string;                 // resident name, or internal question title
  resident?: ResidentMatch;      // absent for internal / unmatched
  subject?: string;              // email only
  snippet: string;               // first inbound message (or first question)
  status: CaseStatus;
  urgent: boolean;
  unread: boolean;
  citationCount: number;
  receivedAt: string;            // ISO
  replyWindowEndsAt?: string;    // WhatsApp only
  sentAt?: string;
}

interface DocumentMeta { id: string; name: string; shortName: string; pageCount: number; url: string; }

interface ClauseRef {
  documentId: string;
  page: number;                  // 1-based
  clauseId: string;              // stable id
  label: string;                 // "§D.3"
  title: string;                 // "Restricted Breeds"
  text: string;                  // full clause text (for callouts / previews)
  rects: { page: number; x: number; y: number; w: number; h: number }[]; // PDF user-space units
}

interface Citation { n: number; clause: ClauseRef; }   // n is per-case

type InlineNode = { type: 'text'; text: string } | { type: 'cite'; n: number };

interface ConversationItem {
  id: string;
  kind: 'resident' | 'manager' | 'assistant' | 'system';
  at: string;
  // resident
  channel?: 'email' | 'whatsapp';
  subject?: string;
  text?: string;
  // assistant
  grounded?: boolean;
  content?: InlineNode[];               // answer shown in the conversation
  draftContent?: InlineNode[];          // resident-facing version for Include
  citationNumbers?: number[];
  includedInDraft?: boolean;
  status?: 'pending' | 'done' | 'error';
}

interface DraftParagraph {
  id: string;
  role: 'greeting' | 'body' | 'signoff';
  source?: string;                      // ConversationItem id it came from
  hold?: boolean;                       // holding-reply paragraph (exempt from citation check)
  content: InlineNode[];
}

interface Draft {
  channel: 'email' | 'whatsapp';
  subject?: string;
  tone: 'friendly' | 'formal';
  manuallyEdited: boolean;
  paragraphs: DraftParagraph[];
  updatedAt: string;
}

interface CaseDetail extends CaseSummary {
  citations: Citation[];
  conversation: ConversationItem[];
  draft?: Draft;                        // absent for internal
  suggestedQuestions: string[];
}
```

**Client-only UI state (Answer screen)**

```ts
interface AnswerUIState {
  activeCitation: number | null;
  viewer: { documentId: string; page: number; zoom: 'fit' | number };
  draftMode: 'view' | 'edit';
  draftHeightPx: number;                // persisted per user
  undoSnapshot?: { paragraphs: DraftParagraph[]; included: string[] };
  freshParagraphId?: string;            // for the flash animation
  pinnedExpanded: boolean;
  composerText: string;
  pendingQuestion: boolean;
  navList: string[];                    // case ids from the Queue the user came from
}
```

---

## 11. Case statuses

| Status | Pill | Set when | Shown in filters |
|---|---|---|---|
| `draft_ready` | blue "Draft ready" | An inbound message is answered and grounded | All, Needs reply |
| `not_found` | amber "Not in documents" | The first answer isn't grounded (holding draft) | All, Needs reply, Not in documents |
| `draft_saved` | gray "Draft saved" | The manager saves, or autosave after an edit | All, Needs reply |
| `needs_review` | blue "Needs review" | The resident sent a new message after a draft existed | All, Needs reply |
| `sent` | green "Sent" | The reply was delivered | All, Sent |
| `my_question` | purple "My question" | Internal case | All, My questions |
| `assigned` / `escalated` / `closed` | gray / amber / gray | F14 actions (v1.1) | All (+ own filters later) |

`urgent` is a separate flag, not a status. It's set by back-end triage (e.g. a live nuisance at night, safety words) and shown as a red pill. It's cleared on send.

---

## 12. Keyboard shortcuts

| Key | Where | Action |
|---|---|---|
| `j` / `k` | Queue | Move row focus down / up |
| `Enter` | Queue | Open the focused case |
| `/` | Queue | Focus search |
| `n` | Queue | New question |
| `Esc` | Answer | Back to Inbox (when no input or editor is focused) |
| `[` / `]` | Answer | Previous / next case |
| `g` then `a` | Answer | Focus the composer ("ask") |
| `e` | Answer | Toggle draft edit mode |
| `Ctrl/⌘ + Enter` | Answer | Reply (opens the confirm dialog if the checks fail) |
| `Ctrl/⌘ + S` | Answer | Save draft |
| `1`–`9` | Answer (not typing) | Activate citation n |

Shortcuts are listed in a `?` help dialog. They're ignored while focus is in a text input or the editor, except for the Ctrl/⌘ combinations.

---

## 13. Accessibility

- All interactive elements are real `<button>`, `<a>` or `<input>` elements. Queue rows are buttons or links, never clickable `<div>`s.
- Visible focus ring: 3px `--accent-soft` halo plus a 1px `--accent` border on inputs; a 2px outline on buttons.
- Icon-only buttons have an `aria-label` (previous/next page, previous/next case, send, resize).
- ChannelBadge has `role="img"` and an `aria-label` ("WhatsApp", "Email", "Internal question").
- Citation chips: `aria-label="Show source {n} in the document"`. After activation, announce through a polite live region: "Source {n}: {doc} {clause}, page {p}".
- Live regions:
  - the ThinkingIndicator (`role="status"`)
  - toasts (`role="status"`)
  - a new resident message (polite)
- FilterTabs use `role="tablist"` and `aria-selected`. Edit and PinnedMessage expose `aria-pressed` and `aria-expanded`.
- Colour is never the only signal. Statuses have text, citation state has a number and outline, and the urgent reply window has text plus colour.
- Contrast: all text meets 4.5:1. Yellow highlights sit behind dark text only.
- The PDF text layer stays selectable and readable by screen readers. The highlight overlay is `aria-hidden`; the clause text is available through the citation's accessible name or callout.

---

## 14. Responsive behaviour

The design is **desktop-first**: 1280–1600px is the target, and 1440×900 is the reference.

| Width | Behaviour |
|---|---|
| ≥ 1280px | As specified |
| 1024–1279px | Right pane narrows to 460px. Viewer page scales to fit the width |
| 900–1023px | Right pane 420px. DocTabs scroll horizontally. Header index text hidden |
| < 900px | Stacked: CaseHeader, then the viewer (max 70vh), then the DraftPanel (auto height, no Splitter), then the conversation. The Queue table scrolls horizontally inside its card. Not a primary target |

---

## 15. Loading, empty and error states (summary)

| Area | Loading | Empty | Error |
|---|---|---|---|
| Queue | 6 skeleton rows | "Nothing here…" | Banner + Retry |
| Viewer | Page skeleton | — | "Couldn't load this document" + Retry; citations still listed |
| Conversation | 3 skeleton bubbles | Starter chips (internal only) | Inline "Couldn't get an answer. Retry" card |
| Draft | Paragraph skeleton | "No draft yet. Include an answer below or start writing." with an **Edit** button | Save/send error banner in the panel |

---

## 16. Component tree

```
<AppShell>
  <AppHeader> Logo · PrimaryNav(InboxBadge) · CommunityStatus · Avatar
  <Toast/>
  <Route /inbox>
    <QueuePage>
      <PageTitle/> <SearchInput/> <NewQuestionButton/>
      <FilterTabs/>
      <CaseTable> <CaseTableHeader/> <CaseRow>[ChannelBadge, StatusPill, ReplyWindowCell]* </CaseTable>
      <EmptyState/> <ChannelFooter/>
  <Route /cases/:id>
    <AnswerPage>
      <CaseHeader> BackButton · CaseNavigator · ChannelBadge · ResidentInfo · StatusPill · ReplyWindow · (OverflowMenu)
      <SplitLayout>
        <DocumentViewer>
          <DocTabs/> <PageNav/> <CitationStrip>[CitationChip]* </CitationStrip>
          <PdfPage> <TextLayer/> <HighlightLayer/> <MarginMarkers/> </PdfPage>
        <RightPane>
          <DraftPanel>            (resident cases)
            <DraftHeader> ChannelPill · UndoNotice · EditToggle
            <EmailMeta/>          (email)
            <DraftBody> <DraftView>[Paragraph(CitationChip*)]* | <DraftEditor/> </DraftBody>
            <DraftFooter> CitationCheckPill · ToneToggle · SaveButton · ReplyButton
          <Splitter/>             (resident cases)
          <ConversationPanel>
            <ConversationHeader/> <PinnedResidentMessage/>
            <MessageList>
              ResidentWhatsAppMessage | ResidentEmailMessage | ManagerMessage
              | AssistantCard(CitationChip*, SourceChips, IncludeInDraftButton|InDraftTag|NotGroundedNote)
              | ThinkingIndicator | SystemEvent
            </MessageList>
            <SuggestedQuestions/> <Composer/>
  <ConfirmSendDialog/> <ShortcutHelpDialog/>
```

Shared primitives: `Button` (primary / ghost / link, sm / md), `IconButton`, `Pill` (tone),
`Chip`, `CitationChip`, `SegmentedControl`, `Tabs`, `SearchInput`, `Skeleton`,
`Banner`, `Dialog`, `Tooltip`.

---

## 17. Suggested front-end stack (non-binding)

- **React + TypeScript**, with React Router (or the Next.js app router) for the routes in §3.
- **State:** server state with TanStack Query (cases, case detail, live updates through SSE or WebSocket invalidation); local UI state with component state or Zustand.
- **PDF:** `react-pdf` (PDF.js) for rendering plus a custom `HighlightLayer`, or `react-pdf-highlighter`. Highlights come from stored clause `rects`; don't search the text at display time.
- **Draft editor:** TipTap (ProseMirror) with a custom atomic `citation` inline node, and a serializer to the `InlineNode[]` model.
- **Styling:** CSS variables from §4. Tailwind or CSS Modules are both fine.
- **Testing:** component tests for CitationCheck, citation numbering and Include/Undo; Playwright end-to-end for F1–F6.

---

## 18. Prototype vs. full version

| Area | Prototype | Full version |
|---|---|---|
| Answers | Scripted, keyword-matched | Back-end retrieval and generation, grounded to clause IDs |
| Document | Re-typed sample pages as HTML | Real PDFs with a text layer and stored clause rects |
| Draft editing | Plain textarea with `[n]` markers | Rich editor with atomic citation nodes |
| Include | Appends a pre-written paragraph | Optionally an AI merge of the whole draft with diff highlight |
| Statuses | Draft ready / saved / not found / sent / my question | Plus needs review, assigned, escalated, closed |
| Live updates | None | New cases, new resident messages, reply window countdown |
| Send | Marks Sent locally | Real delivery, confirm dialog, error handling, audit log |
| WhatsApp window | Static label | Live countdown and template fallback (F11) |

---

## 19. Open questions

1. Should **Include in draft** append a pre-written paragraph (predictable) or ask the back end to rewrite the whole draft (smoother, needs a diff UI)?
2. Is the citation check per paragraph enough, or do we need per-sentence checks before launch?
3. How do outbound citations look on WhatsApp: short refs only, or a link to a hosted page view?
4. Is auto-advance after Reply the default, or a setting?
5. Multi-manager teams: do we need case locking or presence ("Alex is viewing")?
6. Should a single resident message containing several questions be split into sub-answers in the conversation automatically?
