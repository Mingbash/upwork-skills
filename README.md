# Upwork Skills

**Decide which Upwork jobs to apply for, then write a bid that shows what you can do.**

Paste a job and tell your agent about a project you’ve actually worked on. You can get a second opinion on the fit or draft a proposal around the work the client wants done. Two other skills help you spot repeat requests across job posts and write your freelancer profile.

[简体中文](README.zh-CN.md) · [See examples](examples/README.md) · [Quick start](docs/QUICKSTART.md)

## Pick the one you need today

| If you’re trying to… | Use | Bring |
|---|---|---|
| Write a proposal or answer a client | [Proposal](skills/upwork-proposal/SKILL.md) | The job post and your role in a related project |
| Decide whether a job is worth a bid | [Bid Screen](skills/upwork-bid-screen/SKILL.md) | One or more jobs, your experience, and any limits on time or price |
| Find a service clients keep asking for | [Needs Analysis](skills/upwork-needs-analysis/SKILL.md) | A batch of job posts or files |
| Write or revise your freelancer profile | [Profile](skills/upwork-profile/SKILL.md) | Your current profile or notes about work you’ve done |

Each skill works on its own. You can start in chat without connecting an Upwork account.

## Draft a proposal from a real job post

Install Proposal in Codex.

```sh
npx skills add Mingbash/upwork-skills --skill upwork-proposal -a codex
```

Paste the job and a few lines about a similar project. Say what part you handled yourself.

> Use `$upwork-proposal` for this job. On a similar project I built the reporting dashboard and trained the client’s team. They handled data cleanup. Draft the proposal and suggest what I should ask before quoting.

You’ll get copy to review, answers to any screening questions, and pricing notes that spell out the assumptions. If the client hasn’t given you access yet, the draft can quote time from the day you get it. A video outline is optional.

Replace `upwork-proposal` in the command to install a different skill, or use `--skill '*'` to install all four. You can also download a bundle or a single skill from [Releases](https://github.com/Mingbash/upwork-skills/releases) and copy the complete skill folders by hand. [See the install steps.](docs/QUICKSTART.md)

## What happens when you screen a job

Bid Screen can tell you where your experience fits, what it might cost to deliver, and what you still need to check. It starts with the text you supply. If you ask for an account check too, that’s a separate step that needs an approved API for live information. An export or cache only shows what was known when it was collected.

The skills leave drafts and decisions with you. Applications, messages, Connects purchases and profile changes are yours to make. [Upwork’s automation policy](https://support.upwork.com/hc/en-us/articles/43342677368467-Use-bots-and-other-automation-properly) explains the limits on automated access.

## Where the four skills came from

I built these while trying to get better at picking jobs and writing bids. There were plenty of tips about how to open a proposal. I wanted help with the decision before that: could I do the work the client was actually buying, and what could I show them?

Three notes from the original September 23 brief shaped the toolkit. These are translations from Chinese.

> “Listen to different perspectives, identify the shared professional advice, verify it from multiple sources, and distill high-confidence principles and methods into skills.”

I compared existing skills, freelancer accounts and Upwork’s own guidance. One rule that held up was to tie each claim to work the freelancer can actually describe and the buyer cares about.

> “Skills should be reusable; the skill itself must not contain any information about my personal or business background.”

The skill carries the method. Each freelancer brings their own projects, prices and constraints.

> “Record the business processes, pain points, existing systems and acceptance criteria buyers are actually purchasing—not just keywords.”

That became Needs Analysis. A job you’d pass on can still show what a buyer needs. Keep it in the research sample and look for that same problem in other posts.

[Read the original notes and see the sources that informed the skills.](docs/ORIGIN.md)

## When you want to use them regularly

One-off results stay in chat. For repeated work, you can choose a workspace and save your examples, preferences and screening history there. Analysis follows your language. Client copy follows an explicit language request, then the job’s language. [See the settings you can change.](skills/upwork-proposal/references/options.md)

[What we tested](docs/VALIDATION.md) · [Contributing](CONTRIBUTING.md) · [MIT license](LICENSE)
