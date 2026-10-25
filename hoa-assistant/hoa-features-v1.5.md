# HOA & Property Manager Workflows: Automation and AI Opportunities (v1.5)

The current product has three building blocks: a queue of cases, answers grounded in the documents, and drafts a person approves. Many other HOA and property-management workflows are also "case in → check the rules → write something official → track a deadline", so they can reuse all three. They're ranked below by how well they fit and how painful they are today.

## Best fits (they reuse the current product)

| Workflow | Pain today | What the assistant would do | Reuses |
|---|---|---|---|
| **1. Violations: inspection → notice → hearing → fine** | Drive-by inspections with photos and notes, then hand-written letters. Getting the escalation steps right (courtesy notice, then hearing notice, then fine) and tracking cure periods is error-prone, and a mistake can make a fine unenforceable. | Suggest the violation type from a photo, match it to the exact rule, draft the right letter for the current step with the citation, set the deadline to fix it, and remind the manager to re-inspect. | Citations, draft + approval, queue |
| **2. Design-change requests: fences, paint, solar, additions** | Incomplete applications, many emails back and forth, volunteer committees, and a missed decision deadline can mean the request is automatically approved. | Check an application against the requirements ("missing site plan, color isn't on the approved palette, §7.6"), summarize it for the committee, count down the deadline, and draft the approval, conditional-approval or denial letter. | Citations, drafts, deadlines |
| **3. Maintenance requests: "who fixes this?"** | Residents report leaks and damage. Deciding whether the owner or the HOA is responsible means digging through the maintenance article, and the request then has to go to a contractor. | Sort the request, decide who's responsible with a citation (e.g. "roof is HOA, §5.2; skylight is owner, §5.3"), draft the reply, and create the work order for a contractor. | Inbox, citations, drafts |
| **4. New owners and home sales** | Every sale needs a disclosure package by a legal deadline: documents, balance, open violations. New owners ask the same questions over and over. | Assemble the package automatically, flag open violations, and answer new-owner questions from the documents. Optionally send an onboarding checklist (register pets and vehicles, get a pool key). | Documents, Q&A |
| **5. Board meetings** | Building agendas and packets, posting notice on time, and writing minutes from memory or recordings. Action items get lost. | Draft the agenda from open cases, check that the notice period meets the bylaws (§4.2), turn a recording into draft minutes, and pull out action items as follow-up tasks. | Citations, drafts, tasks |

## Good automation, less about the documents

| Workflow | Pain today | What automation or AI would do |
|---|---|---|
| **Overdue dues** | Reminders, payment plans, and the legally required steps before a lien | Reminder sequences and step tracking, with every legal notice approved by a person. High risk: keep it conservative. |
| **Contractor bids and insurance certificates** | Comparing bids that use different formats; insurance certificates expire unnoticed | Turn bids into a side-by-side comparison; track certificate expiry and request renewals. |
| **Invoices and bill payment** | Manually entering and coding invoices, and getting approval for anything over a set amount | Read the invoice, suggest the accounting code, and send it to the right board member for approval. |
| **Announcements** | Notices, newsletters, translations | Draft from a template, translate (Spanish especially), and send by email, WhatsApp and the resident portal. |
| **Rule changes** | Old rules that contradict the CC&Rs or new state law | When a new rule is drafted, flag conflicts with existing clauses and summarize what changed for residents. |
| **Legal calendar** | Required dates: budget disclosures, annual meetings, filings, elections | A per-community calendar of required dates with reminders and draft notices. |
| **Elections and votes** | Quorum tracking, ballot timelines, secret-ballot rules | Mostly workflow automation; AI drafts notices and results summaries. |
| **Phone calls and voicemail** | After-hours calls that go nowhere | Transcribe calls into the same inbox as a third channel. |

## How it could grow

- **Phase 1 (now):** the question inbox. It proves that grounded answers and human approval work.
- **Phase 2: violations and design-change requests.** Both are new kinds of case in the same Queue and Answer screens. The draft becomes an official letter, and you add a deadline/timeline panel. This is the biggest time-saver, and it reuses the most.
- **Phase 3: maintenance and board meetings.** This adds contractors, work orders, and recordings turned into minutes.
- **Phase 4: home-sale packages, overdue dues, invoices.** These are more financial and legal, need connections to accounting systems, and carry higher stakes.

## Principles for all of these

- **Follow each state's law:** California (Davis-Stirling Act), Florida (chapters 718 and 720), Texas (Property Code chapter 209), and so on. Deadlines and required notice steps differ by state. Model them per community, and cite the statute the same way you cite the CC&Rs.
- **A person approves anything official:** fines, liens, denials, legal notices. The assistant prepares, checks and cites, but never sends those on its own.
- **One case history per property.** Violations, design-change requests, questions and maintenance for Lot 117 should all show on one timeline. Managers and boards need that history when disputes arise.
- **Validate before building.** Ask 5–10 managers which three of these take most of their week. Violations and design-change requests usually come up first, but your market may differ.

## Possible next step

Prototype the **violation workflow** on the canvas: a new case type in the existing Queue, with a photo, the matched rule highlighted, the escalation timeline, and a draft courtesy notice.
