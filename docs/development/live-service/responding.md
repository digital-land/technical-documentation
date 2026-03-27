## Responding to a Live Service Issue

### Scope of this Document

This document is intended to use as useful guidance for those responding to live service incidents. 

### Initial Report

There will be a post on the `#planning-data-infrastructure` slack channel, reply or give a suitable emoji response to say indicate "I'm on it."

Read the report carefully, including any related log entries.

Now is a good time to stop and take stock. Don't charge in all guns blazing. It might be a good idea to make a cup of tea.

### Initial Assessment

With your tea or other beverage in hand, methodically and carefully look at what's happened. It might be something that has a fairly obvious cause, or it may require a bit of investigation. Resist the urge to 'rush through' this step, but try to give an update as soon as possible.

Your initial response will depend somewhat on the nature of the issue, but at the very least give some sort of indication as to what you believe the problem to be. This could be a general synopsis and that you're still getting the details. eg "Collector ran out of disc space, trying to replicate locally", or it could be that that you have enough information give a more detailed explanation of the problem, eg. "error in input file caused digital land builder to fail.". In the latter case, the next steps may well be known.

### Initial Response

You should post a reply to the message with the initial assessment, the next steps and an approximate time frame for the next update.

This lets people know what the problem is, what steps are being done to address it and when they will hear more. This lets anyone who might have relevant information to let you know (eg. we saw something similar to this here), if anyone sees any potential side effects they can let you know (running that locally might take ages, maybe try a small subset), and when they will hear more (which should hopefully at least reduce being hassled for updates).

If you are still investigating the next steps should at least outline the area(s) of investigation. When the investigation is complete, the next steps will be to address the problem, as above.

### Working on a fix

At this point, you will be working on addressing the problem. The thread informed of progress and next update. When the work is done and ready to merge, create the relevant PRs, and post them to both the PR channel and the thread. This will also serve as an update, eg. "Code fix ready for review".

Work methodically, **DO NOT** be tempted to shortcut checks, tests, and PRs. If full code testing cannot be done in a reasonable time frame, make sure you do manual testing, and create a ticket in the LS backlog to address the tests.

### Deploy the fix and re-run

When the approvals are obtained, you can deploy the fix(es) and re-run any necessary processed.

When you start this, give an update for the deployment, and then another for any rerunning. 

### Results

Report on the results of that. Did it work? Great! If not; make another cuppa and see why not. Proceed from initial assessment (above).

## Key Points

### Keep Calm

Don't rush, don't charge in all guns blazing and miss something. Be methodical. Don't take shortcuts, don't skip checks in a rush to get a fix out. Better to delay a fix by 30 mins than result in 4 hours of fixing the fix.

### Keep People Updated

Give updates at key points, and always give a "next update by ..." time. If something takes longer than planned, try to get an update in as soon as you know. You don't need to post a running commentary, just the key points. These are just ETAs - don't let people hold you to them!

*May the odds be ever in your favour.*
