Okay, we'll get started with the Omnia Provisioning Team Sprint for demo. So, I mean, just wanted to call out everybody's efforts in this sprint, actually, because,

This was actually from provisional team point of view. This was a very much critical spring, and I think we have done a very good job, as I think, and their team has done very well. So there are a lot of

I think we have worked on 5 epics in one sprint, that is something we were not normally used to do. Five epics, we were working parallel in one sprint, and we were able to complete most of the things, and thanks to everyone who has worked on this, so I will…

Yes. Yeah. So, we will, I will just…

goal one by one. So, so… so first we'll, have a nary milestone, three tasks where we have implemented, passcat log, generate input file by way, you know, then local repo and playbook virtual by Rajesh, and then build image by Preeti and, and support by Kratika, and…

complete GitLab configuration has been done by Milesha, then, testing support by Balaji, and… so then we have the Omnia Core upgrade task, and I was, really appreciate, Sajini and Midlesh for the, they have came up, and they were able to, do a great job, like.

I was initially thinking, basically, we can have a basic upgrade flow. I was pulled… even… we have completed the story, and we have even pulled in the dates for the upgrade task, so thanks for that, and even Sushmita was able to pick up the test scenario and was able to complete it on time, and…

Then, Netra was able to, handle that telemetry individually, and drive that complete telemetry for add and remove node, along with Sashi, and thanks, Sashi, for that extended support.

Then, due to time crunch over me and SFM, there are some changes to be done for the playbook, so that I have taken myself, and, Prashant is working on the testing, and,

we have completed the additional packages, and and Vasan was clinical on all the document updates we have each and every sprint, so thanks, Vasan, for that, and…

Yeah, so that's the main agenda, and it's just to,

start before… just wanted to have that burndown chart to show on everybody, so… so, this is the current burndown chart we have, and I think we have done a…

good job in this print for this, burndown chart, because, initially, we started with the 117 story points, and, I know it went a little bit deeper, in some places where we had an issue on Friday, or there are some issues, but mostly it went down, and we were almost on the line, and,

So, initially, it started with 117 story point, and, the total story point for this sprint day alone is around 137, 130, and there are many people who have worked on overnight, night, like, 10 points, people have worked 15 story points, 16 story points, like.

So, thanks for everyone, and yeah, I'll hand over, as, Devils and Under will, start with the upgrade flow. I will start, make them, Saojini and Midlesh get started with upgrade flow, and then we will get over to the, NRE Milestone 3.

Thank you.

No, total we completed, 141, it is there, no, yeah.

We completed the original scope, what we do. Original scope plus additional scope.

Yeah, this was happened because everybody was contributed, like, and we had to push everyone to get this. Yeah, thanks.

Thank you all.

I let South Jinier Dilesh get started with the upgrade.

It can join this one.

Soon, so on.

So I'm going to join.

Okay, mate.

Hey guys, how you doing?

Hello, everyone. Today, I would be showing the demo of the upgrade flow.

Thank you. Thanks, Speaker.

As we all, in the upgrade flow, we have, come up with the three new options,

That is, the,

That is, upgrade, rollback, and the version. Now, we have included these three options in the help command, as moving forward.

We have to download the new Omnia.sh shell script, and now, we can see that, the user first currently will be in the version, Omnia version 2.0.0.

We have come up with the command now. We are getting it from the metadata.

So, this is existing in the PD today? No, 2.1 onwards. 2.1. We are releasing this in all three new features in the 2.1. Okay, so this…

You gotta…

deriving this value, or we are storing this file? Deriving. We are storing and deriving. I mean, yeah, it's stored in some file. Now, 2.0 RC… 2.1RC1 is deployed on EAS.

That we cannot get it. We won't have that, right? Yes, yes.

Okay, so when they take the 2.7GA,

RC2 onwards, you will see this.

RC2 onwards, they will be able to see the 2.1 RC1 also?

No, no, no. This is a specific tool, or…

2.1 or not, but this shell script… because that shell script is different, then. This is the updated now. Okay.

The user would be currently in the Omnia version 2.0.0.

Then, if we check the permanent, containers running.

Alright, we can see that Omnia Core 1.0 container is being, as of running currently. Now we have captured this, after the prepare OEMs, after running the Playbook Prepare OEM.

And then, if we are now logging into Omnia Core Container also, we can check the, metadata. It is also with the Omnia version 2.0.0.

As of now, the input files now, in the Omnia version 2.0, the input files are the default, input files.

These are the… this is the default, input file of the version 2.0.0.

One of the prerequisites of the upgrade or the rollback, flow is that the image, the image for which, the user is being upgraded, it has to be locally present. For that, the user has to run the command build images to get the image locally present.

One thing, to call out that here, if you see 2.1 tag, so that for now, we have decided that Omnia, for every version, the first two digits will be taken as the core tag version.

Excellent.

He's anxious to present. Get you a chance, don't worry. So, Omnia Core 1.0 was there in 2.0, it'll become 2.1. So it will jump from 1.0 to 2.0. Only for the Omnia versions 2.0.0, we have kept the default as Core Container Tag 1.0. Any other versions, next all versions, we are taking the first two digits.

Yeah, keeping it as code, I think.2 will give you only have code in .2.

Huh.

Then the upgrade is actually a two-step process. The first step would be, running the command omnia.sh upgrade, hyphen hyphen upgrade. Here, it will display to their users the current Omnia version which the user is being in, and the core container tag of that version.

And then it will show the available upgrade options. And now, as of now, we have created a list file, where it has all the Omnia versions being present.

And, we are checking that any, now we are checking when upgrade, function is being called, the versions above the upgrade is being listed in the available upgrade options. User can, go to any, option which is being… getting upgraded.

Huh. Huh.

Now that we will see if we can do it. For now, we… we have introduced the framework. We introduced the framework enough.

My 8th, At this point in time, be very clear when you're stating.

that we will go end to N plus 1 only. For now, it is only N plus 1, but the framework is simply manual in any time if you wanted to do anything, but if it is NNN plus 1, this also will work. But here we are displaying is the next available version we are displaying here.

Because there can be some time, there can be patch version. So, the reason being, listing the available version is, you can have a patch version.

Beautiful.

Beautiful.

Do not zero.

No, no, not 2.2, but if there is a patch version, that's it. Yeah.

Do we support the integration from the coup?

Not one, or to the patches.

And that's right, if we have to support that patch version upgrade, that is simplified.

We need a proper strategy.

Yeah, so that… so we… so for now, what we have done is we have done a framework. So now, we considered in mindset that it is always N plus 1, but the framework is ready to list the available version, and… Make sure it cannot go N plus 1, anything beyond that. Okay.

So, Sujit, like how we had for OMSA, we need to have a proper documented upgrade path, or a rollback path, including how to deal with the patches, right? Patches have to become inclusive

In the next…

in the major version. Yeah. Right? And if, ideally, patches also should be cumulative. If I have the second patch that should be built on top of the first patch, that's preferably, unless there is a violent reason why it should not be.

Okay.

We need to document that first, we need to review that with Peter and everybody else. Only then we can implement the framework to do that behavior.

Yeah, that we will come… actually.

This script is downloaded by user, and there was an issue in Word, we will keep that JSON, so that is my reason we were going this approach.

And then user has to go with the… which the… which of the version that he's going… is being upgraded to. Then it will have a pre-upgrade validation, which checks the… whether the image is being locally present or not. If not, it will fail in the phase one. And then, the second phase is the approval gate. It is…

getting an approval from the user again to go forward with the new version, the targeted Omnia version. Then it is also stating the backup destination, where the current version which it is running.

where that version is being stored. And then, if it is being approved by the user, it moves forward.

And then the sheikh.

It's a really good step.

then it'll be… No, typically in the cleanup way, Excel is going to be… No, not this NFS.

That is slamming case, okay?

Then Phase 3 is the backup creation, where that folder would be created, and Phase 4 would be the container swap, where it would stop the Omnia Core Container 1.0, and would start with the 2.1 quadlet unit, and it would check all the health metrics of that container.

And how do you verify the integrity of the backup data?

Backup data, very integrity, like, we are keeping whatever that input file in that backup folder for now. I mean, we are not… whatever in the user's current NFS share, we are just copying to NFS share.

So, if that backup is not being created, it will fail in that stage. It will not…

That is coming in the next tour.

That check would happen in the next, wherein the next step would be the…

Not being the same… hierarchy.

Right? It should not be the same… ideally the same partition, if you will.

Okay. Idiot.

So that by mistake, if somebody blows it away, you can't restore it back.

Currently, we have… we didn't take an extra input. Whatever user has given, the same NFS share has been used for now. I mean, we have not taken a… NFS share is okay, but it should not be in the same as the fold, doesn't it? No, hierarchy is different, but same NFS share.

Let me take a different folder. Different folder.

We need to make sure no manual or any bug doesn't remove your backup.

Currently, yeah, it's kept separate like that. Every folder we kept like that in NFS, so that's really kept in that NFS. Yeah, I think that's where this, upgrade strategy, I think we need to really review how to ensure integrity of the preparation for the upgrade.

Okay. But everything is different, or you find?

It should be okay, but what I'm saying is, there are multiple folders that we are taking backup of, right? All this backup has to be at the time stamped.

It cannot be this one, right? So, what is the way we are ensuring that nothing, no user changes are triggering at that time of taking the backup?

Right? Ideally, the… this one put it in a maintenance mode, and then I start my upgrade. Prevents anybody from coming in and doing it. But these are all flag files. How do I prevent the…

users from, editing it while I'm upgrading my…

Yes, prerequisites you are writing, right? We are doing some operations, like, we have…

Now, that we said, we'll take it from the next one, currently this one. Yeah. Volume. That we are…

We have documented. And we are not yet done. We are going to do next. Document. Which phase you should run the… That we should go with this…

That document should go with this one.

But it should be automated in the next one, where when you say upgrade, it needs to check for that set of things, programmatically if possible, and say, hey, this is not in that state. Like, when you shut down your machine, it will say, hey, these files are still open.

Right? Exactly. Exactly same behavior. Just like an Omnia stage, currently we don't have Omnia stage tracking.

Whatever stages are Omnia executed, is any Omnia playbook is in running.

That is why we are having that issue. Currently, that is not there, but we are planning to do that and make it ready for next year. Whatever is a safety net we can build, right? It could be as simple of, okay, grasp for it in DPS, and see if there is anything active.

Right? Then you say, okay, it cannot be.

Right? So, whatever safety net we can provide visibility to. We may not be able to enforce it in this point in time, but at least visibility to saying, okay, you're taking a chance with the state of the backup. Okay.

Okay, the process for this is simple, but the impact of doing something wrong is catastrophic. Okay.

Obviously, it is only documentation. Ensure all these things is verified manually before you start. Yeah, it's upon the user not to run, you know, the playbook.

Also, in the documentation, right, you may want to capture, like, what services we trusted, During that period.

something like, build image in an R2, regularly, but that cloud will be running all the time, right? So authentications are always sitting in your VIN. No, not today. I think only 4 content here, but when you are… Doing that something? So you need to…

Yeah, no, this was a lot of the HA partner.

Before we even become 18.

We don't have roads, and we…

Make it active and come back. Have we not adjusted as part of the HRD?

Which one?

Yeah, great path. All the questions that you're getting.

Have we not addressed this as part of the HED?

No, HLD, whatever, this was not there, but these questions, I mean, this, whatever we have discussed now… How did we approve the MTR without these things?

No, it was, whatever the basic flow only, we have captured in HLD. Whatever you play, whatever you have, implemented, you have captured in the HLD. But we don't write HLD for only one section of the behavior, right? HLD is all-inclusive.

HLD has the… I mean, we have agreed upon that. For Q1, we will go only this, behavior.

Yeah, currently, we have… we had not disposed on the HA department.

This is Q1 scope. Not for the documentation part? Yeah, that is fantastic, yes.

Thank you, Pardo.

Oh, yeah, that's what it is.

Major vacation?

No, no, OEMH is currently not there, right? Yeah, that's why it's whatever this commence. I understand that part. My point is…

How consciously are we calling this design?

to be not requiring major rewrite if I bring in OAMH.

Thank you.

Neeve.

That is, like, we are… I don't think the really major thing, but this… that we are… Not, I don't think. That night has passed. Yeah, that's…

Currently, we have not checked the OEMHS perspective, but yes, we need to.

Okay, guys, this is what we were talking about in the last one.

Right? Where the state of Omnia is no more a development stage.

Right?

the gatekeepers, I would really request you guys to be really, really stringent on what functionality we are approving from a HLD perspective, because if you guys do not incorporate those safety checks.

you're exposing yourself to a very big trouble.

Right? In the field, if it breaks, imagine EAS is in progress, and you're upgrading to 2.1, and it corrupts the existing cluster.

Your recent 3 months of work.

Right?

We are no more in that, development phase.

We are in the production, for all we know. We need to really be ultra-cautious in our designs.

Okay.

We'll check OEMH if something changes.

The next step in the upgrade would be the running of the playbooks, which will take care of the update of input files and the update of internal configurations that would be explained by Mithilish.

It's…

Yeah, here we can see upgrade is successful, and we are already inside Omnia Core now.

Let's a good pass.

Yeah, you can see that metadata has been updated to 2.1, and the backup directory also has been created in the metadata.

We came outside the container, and we are just checking if the tag has been changed, and it has been changed successfully.

Also, the version also has been changed to 2.1.

Can you send that script again.

Version you can run. But one more thing I wanted to check is, like, here we have not handled its RC1, RC2. Currently, even for RC2, we are planning to give Omnia version as 2.1 only, or we want to keep it specific 2.1 RC2 only.

That is… because currently, then, every time you need to keep changing this. Is this okay, then we can do it. But this will become constant effort for every tag. So, this script…

Is, really specific.

this… White.

Because this is attached in the Omnia GitHub, that's why. So, you have already cloned the repo.

before you… Shell script is… I would save the rep. I mean, share script is actually inside the repo. That's what I'm saying. You have already thrown the repo for 2.1 when you initiate the upgrade path.

No, but that's shell scripted, but that file, you are…

So this is Dominator?

Capture America.

Okay, 13.

Gary's still thought, right?

I need to initiate an upgrade from my current installation.

Right? And current installation has no way to know what is my latest and what is available. Correct? But I can query for it.

Huh? Perfect.

No, currently we don't have that.

Begun?

We can query GitHub. Query GitHub for whatever is the latest ones available. Versions we can query.

Peyton has put this requirement for Q1.

like, how to, show, like, if there is a new machine is available, the kind of notification, right? Considering, the current site, I removed that for the keyword.

That's okay. It's already, like, requirement details. Okay, no, my thing is going a little bit more complex than just telling me that there is a new NFL version.

Right? I need to be able to display, hey, what are the… because if I'm on 2.0, and I have released 2.3,

Right? It shouldn't just say that I have a new version. If I am initiating the upgrade process, it should be able to tell you these are all the versions that are available for you.

Why do we throw it in the code?

Booty.

Okay, I think this speakers and all that conversation. Ravi, I think we need to be able to…

more, if there's a requirement, then we need to see how we need to…

We need to notify customer training. Notification will be possible, but I think upgrade for upgrade only. Look at it this way, right? Look at it this way. It could be a simple command in my current installation, which I run before I clone.

Right? Which can go and come back and say, hey, if it has net connectivity, assume that OEM has net connectivity.

it should be able to say, from the metadata that is there in the GitHub repo, what are the options available, and is there any R dependency on, I can't go from N to N plus 2, or N plus 3, or N plus 1 only?

those kind of patches available. That information I should be able to query.

Before I even clone the code.

My point, Pilty, is no, it's not about gathering these thoughts. These are not new thoughts.

So, Ethan…

Yeah, that's right. Actually, because of the… before we go write code for these things, we should think about these things, right?

No, that is… that is true, Dr. Viscent. I'm not seeing that mindset that, hey, I will…

thing from this perspective, we have… we do not have these capabilities today, right? That I am not seeing. That's where I'm looking for.

There is a time crunch also. Time trench is there, boss. I'm not saying that we covered all of that yesterday. What I'm saying is, are we considering those, requirements? Where are they considered?

For the, customer marketing consequences.

There is a reflection.

That's what I'm saying we need that discussion, separately, to understand exactly what is Mansion.

Okay, and to answer the first question, yes, that requirement is considered, but, we've talked about fear and scale.

That's fine. If you have considered it, fine. It is considered.

Okay, now inside the 2.1 core container.

We can see the input file has not been changed yet, because it is part of the second stage where we run a playbook.

Where the user has to run a playbook.

And also, the backup directory is also created inside the container, where 2.2 inputs are stored.

So this is the… this is one of the input files which is present in the backup directory.

Now, the user has to go to the upgrade folder.

And has to run, has to, run this command, for the second stage to occur, which will basically migrate the input files and the config files, which are present in 2.0 and, 2.1.

We can't be taking backup of the original input files in the container that I am upgrading. That folder is NFL share.

Currently, all that input, everything is in NFL share. That's what we, I mean, we have discussed.

That's what it is… it's a different directory than Fisher.

Okay.

Not that, right? It's like I'm sitting on the tree branch, and I'm cutting the tree.

I'm cutting the branch at the root.

So, this is a 2.1 code? This is a 2.1 container running, right? 2.1 container, correct? Correct. So, I am in the new tree, and restoring the leaves on the tree.

That I planted now.

So, is the container running? Container is running. Container is running, now we are copying the old files. Old input files to new.

Why do I need to bring… why do I need to stack the container for me to restore the input files for that container?

No, no, because we need to transform the… there are a lot of inputs we have introduced in 2.1, which is not there in 2.0, we need to move that info.

Yeah.

Yup.

So, actually, our workflow is tied up with Omnia Core, our current 2. Our complete Omnia… every Omnia workflow is tied up with Omnia Core currently.

I think we need acceptance.

I think it should be part of your…

See, this is like I brought my new engine, I have replaced my new engine, and I need to swap out some, no fuel injection system into that while riding that vehicle.

I should prepare the new vehicle, I would say, before I start up the new vehicle. This is like you're driving the container, new container, and you are, you know, changing the spark plug, or you're replacing the carburetor, or something, by replacing the input file.

Then this thought process coming under the user behavior, like, well then, we really need to give this to the user.

Yes, yep. The same processes are opted for up in the NFL.

So if we say that we can't do that naturally, we have to have the same flow for the pastel.

let's, in the interest of time, let's… I'll park my questions, I won't ask any more questions, but I think there is a basic disconnect in what I think, because my worry is.

if I am modifying the input files that drive the behavior of the container, right, in runtime, yeah, I'm taking 2.0 input parameters that were stored, and I am updating that to 2.1 state. That is because of…

Yep.

Yeah, that… whatever… this is further upgraded.

Yeah.

Because otherwise, user has to fill all the input which he already filled in 2.0 again in 2.1. That's right.

If I cannot do this input parameter update.

Update of the input parameters for the subsequent containers.

I should not even go through with the, you know, upgrade process. I should check that before I initiate this upgrade to 2.1 from 2.0, if there is a chance of any of the input parameters that I am modifying.

If it is going to break the building of some other container that is dependent and will be started from OAM Core, right, then we should not even go through the whole upgrade process. It's a two-step process, that's what we told you, yeah. I think we are out of that.

they're not on the same Keep going.

After the input migration is done, the user will be provided with details regarding how he has to re-provision the clusters, and what steps he has to follow next. So, here you can see,

the user has info about what new fields have been added in the input files in 2.1 format, and what he has to go and change manually. And after that, what he has to do to reprovision the cluster, like running local repo, then build image.

Then discovery.

So this is a mandatory step that we need to rebuild after every upgrade.

I mean, for… it is not mandatory for now, what is happening? We are not… for now, for Q1 specifically, we are not supporting, any other upgrade than core container. So, already cluster is up means you are actually… if I told you how to use cluster, we have an add node feature, or some new feature we are using. So, ideally, you have to…

Completely reprovisioned the cluster, to… Use that, because,

We cannot have… we have not done any framework from 2.0 to do this one.

Because only core container we are fetching. We don't know the state of other container or cluster, what will happen.

Because the scope is limited to core container this time. That is, input is of… input only, it will change now, but I'm telling, if you want to…

we do something on your cluster. If your cluster is idle, it is okay, you can keep continuing your cluster, but if I told you you need to use any of the 2.1 features, you need to re-provision the cluster.

If you want to use… let's aware that, you know, we are upgrading OpenChim here as well.

We either have to color all the input OIM again.

And I can later on that, it'll come in upgrade only. This playbook only will do that old thing.

The same playbook. See, the reason why you're getting so many questions is upgrade is a very convoluted part.

Right? It's a very tricky one to get, first time correct.

Yeah. Right? So, you will get a lot more questions as we continue to do this. And some of them are round questions, some of them are missing gaps, right? Both are there. Yes. Okay? So, it's not like we have done a bad job. We have done a great job, but

some of the things that we need to think through before we walk down that path, because once we put on 2.1,

You're setting stone in a way of how to expect upgrades.

Right? We want to be clear before this goes out, what are those things, and how it will impact your next upgrade from N+, no, from 2.1 to 2.2. That we need to think through.

Okay? That's why you're getting a lot of the questions.

I think I will say that word 2, 3, 4 is not needed, because he knows already what to do with that.

That does not change, right? No, we are telling you, you don't need to run Prefer OEM. What all the steps you need to follow? If you see obtainer and all are the new features which came.

So, if you wanted to do some new feature, then he has to run the local rep onboard. So, for that, we give on that, okay, there should be a summary, what we have updated, and all that thing.

So, anything what we do on OIM, right? Let's say open Chinese upgrade, or bulk upgrade, or ARP upgrade, we'll say that only this is upgraded. Now, with the wrong user flow, that will never change. And this is the next step after upgrader. Why am I putting open up again? Because for new features.

It's not mandated. For new features. If you are asking to run all of this, that is as good as the installation. For new features?

If I want to use something, for example, if I have red something, then I'll run local for now. You can't force me to run local… No, no, no. We are not forcing if we…

Anyway, that's what… in case if you want your information. You don't have to say that.

You know what? But even another thing, right? People get… we get a question.

22.60.

We get questions like that, Sujit, like.

So we can mention, like, I think that's why you return, re-provision the cluster, if at all. We can make it as optional there. Yeah. You're feeling that I have to run everything. No, we'll keep it as optional. We will make it as optional.

Now, it is not the… I'm telling…

to run all the playbooks in sequence. Let's say that's under the… No, no, no, no.

Yeah, that's what we want.

See that? When I run, upgrade LEGO to do whatever it wants.

But the log scheme you don't prepare while local record, that is?

A local rep… this cluster reprovision is very suitable. By the way, both…

Downloading the packages. It doesn't do anything with the pump.

Okay, I think we invested time.

So you can finish slowly.

Huh.

Didn't play?

But… Yeah.

Please be explicit which directions you are talking about, because you are using NFS for many things. We are for your backup, you are using… simply derogatory enough for everything to do by itself. Okay. So be explicit.

Okay, this message will revisit the rest of the pictures, but just one question. I run that over in our message again.

take what you say, and… It will tell already upgraded. That will come. Captured.

Okay, excellent.

This saves the nation ever been.

Here we can see that inputs have been updated, and in 2.1, IB network is a new thing which comes in network spec, and it is set to default, and user is given, you know, what new things have been added.

Which you have seen in a previous message before.

Oh.

This is another input file, where config sources… another way of, you know, mentioning config sources has been added.

Password data back.

Can you continue?

For the rollback, thing, the same, command would be there, omnia.ssh-rollback, which, gets… which lists, again, they are all the available versions which can be rollbacked.

And, user has to select for which version he is getting rolled, rolling back, and then it is again asking user approval, to roll back again.

And then the directory, and then it will stop the Omnia Core Container 2.1 container.

It's the one for which we just went back, right? There will be no other versions of… But we are just displaying the version.

To do this.

Now, if you choose to go and press 1, and press 2, Right? If he's a bat.

Though you may… if they have operated more than one batch, you may want to roll back some clients.

step.

Positive… Awesome. Today, we want to enforce that, so that we have a little bit before control.

But I think they'll put the foundation, too.

Mop, skip, and jump, if possible.

But we won't recommend that.

One step backwards at a time. Like, one at a time.

Okay, so it should be there. So, will you go inside again, you expect to run some left playbook?

Rollback is a one-step process. How inputs will be restored? It's already a backup folder, it's already there.

Take time.

That's the book.

Backup will be present? Where all the input files and everything will be present. I think there is some discrepancy we discussed. Also, we need to explicitly take care the way you're doing the enrollment.

I'll tell you, I'll do that.

We're following up evening.

Because, there are new input parameters we introduced. To execute further, features, then why you want to copy? No, no, no, then your cluster is in dangling stage. Whatever the default input and the actual input user has given is in backup folder.

That's why… No, it's implicit. That has to happen implicit. That's what I'm saying. Currently, it is, we have one playbook, that is. Yeah.

Once you are inside, everything should be the latest. From there, you take it to start the playing on the… Currently, there is one playbook to do that. It's possible to do that? I tell you how to do that.

That's it.

And then, let's say, in the rollback here, I have the problem. On the upgrade field, something fails, then they would go back to the previous session.

That can be anything, let's add an online feature. I want to roll back, right?

We can go back to detail.

You want to see that error message, or we'll continue the next one?

Like, scenarios, like, upgrade is run twice.

So, we have just captured the conflict between two upgrades. In… if a user is running

upgrades, when one CLI and there, again, one more user or the admin would be running one more upgrade, it would, in parallel.

It is a conflict between when an install is running and other install is running. When two upgrades are running, it would say that an upgrade is already being done, no?

And then we have captured conflict between two rollbacks also. When already a rollback is going on, user cannot do again a rollback.

It may be that the process is dangling or something.

I need to find it on YouTube and take…

Two at which we're trying to upgrade simultaneously, because generally it would be one… I've seen the ticket.

If connected.

Okay.

We really want to test the… review the test plan for upgrade.

Okay. When can I get food? Yeah, I want to visit.

Okay.

Okay, everybody can see cut.

I will take it tomorrow.

Sir?

There are many other features. There are many other features, we have only 4 minutes. You want to schedule another meeting.

Oh, yeah, let me take long. Yes. And get even prepared.

We'll have a separate session tomorrow for Larry, then.

Can we, the next one. Finish.

So, as we know about the NI project, that we would have to run pipelines, and most of the work will be running pipelines. So, to host those platforms, those pipelines, and where we want to use them, we have chosen GitLab as a,

platform. So, as per GitLab, we can have two kinds of setup. One is, like, we… the client does not have an external GitLab configured on its own, and they want us to configure it, whereas the other way can be. They have their own setup ready, and we just want to integrate with them.

So, as of now, as part of this sprint, we have worked on the hosted GitLab, which is, like, the user will provide a note, and we will set up the GitLab end-to-end using our playbook.

In the next screen, we will cover the external, which is already… which, the GitLab that is already configured. We can connect that.

So I'll start with the GitLab… hosted GitLab. So I'll just give you a quick overview of what GitLab is. So GitLab is a platform where we can run the CICD jobs and where all the pipelines can be executed and can be… it is similar to how we use Jenkins on the similar grounds.

So, the pipelines to be executed, we need GitLab runners. So, basically, GitLab is the platform, and the person or the instance that actually does the job is the GitLab runner. So, whatever pipelines run, and wherever the jobs get executed, they get executed inside the runner.

So, for a quick overview.

I'll tell you, like, what is exactly happening where. So, we'll get the inputs from the user, there will be an input file, which will be present in our core container, and there we will give all the input. It would be placed similar to how we have the other, input files, like provision config and the other files. We'll have a GitLab config. I'll come to the file later.

So, we'll give the inputs there, and we have a GitLab playbook there. So, we run the playbook with just the inventory. So, the prerequisite of the GitLab server is that we want us

press node, which is installed with RHEL 10, like, it… it should be a disk full, node, like, OS installed, and the version should be RHEL10. And, once… and it…

it should have internet connectivity. So, these are the three things that we are requesting as prerequisites, and the SELinux should be disabled. So, if that is, that server is ready to flash with rel 10, and SELinux is disabled, and internet connectivity is there on the server, we need to just give the IP of that node in the inventory, and we can get the

playbook running. So, if you see here… I will put it in permissible mode and still operate.

I think it should be working, I haven't validated that, like, we can validate that part also. This current setup, I validated with the disabled part.

there was one or two problems, maybe even enable can be configured, but we need to dig deeper into it, but that's, possible. Initial framework we tested. I just went with the happy path for this flow. Why do we need internet connectivity on that server? Because it is kind of…

So, only for that purpose. If we have the repos and everything already available there in the air gap kind of a scenario, then we don't need the connectivity.

So, for initial setup, we have tested with, internet.

So, yeah, so the flow will be, like, once we have that server ready and we put it in the inventory, this is where you put the IP, and we have to run this playbook, which is, hitlab.yaml, with the inventory that we have provided. And once the playbook is executed, this will be an entire flow of the playbook.

And then once it is completely executed, it will show a small report. This is a small report of what all configurations are there, like, this is the… how we can access the UI, what is the port they have used, what is the project name.

That we have configured, what is the odd token? So, whatever details that are required for the user to know, we have printed it as message. So, as part of the playbook, what we are doing in the background, what the playbook will take care, it will install the entire GitLab, it will configure it with whatever… with the basic configurations we have, there are a lot of configurations

That can be done on GitLab. So, based on the user requirement, whatever he wants to get it done, there are configurable parameters, and once you do that, it will do the end-to-end setup. It will help you launch the UI, then once you're able to launch the UI, it will also create the runners. So the runners on a backend, how they are implemented, they are nothing but podmin containers, which are running on the GitLab

host that external node, and those runners are responsible to take up the jobs. So, there is no manual intervention, everything is created as part of the

playbook, it will go and create the runners. So initially, if you see, there were no runners while the playbook was executing, it created one runner, which is called as the OMIA runner, and this is looking as online. So if it is online, that means it is active.

And once that is done, this, like, we can go on the UI and see how the runner is and what is the project. So, as part of the project, we also create a project. This name is also configurable. The user can give whatever name he wants.

This will be our input. So, we have created a OMIA catalog repo in the GitLab. So, as part of that repo, there will be two files initially.

So, one is the CI.yaml, which is the actual pipeline file, where all the APIs and everything will be called, and the other file will be the catalog rel.json.

So the catalog rel.json for NRE framework will be kind of the entry point where all the parameters and packages and whatever configuration will be there will be as part of this file.

So, while showing the NRE flow, we can get more into this part. So, this is kind of an input file, where the user is supposed to make changes. And as of now, the flow that we have developed is that whenever a user is changing this file, like, there is a change in the catalog file in this folder, it will trigger this pipeline.

So this definition pipeline, it will trigger. I'll show you how it looks like.

So, once you execute, like, do any change, for example, I changed the version from 3.0 to 4.0, it will go and trigger the pipeline. So, you can see here that pipeline 14, like, it has been played multiple times, that's why it's pipeline 14. So, it will be triggered, and once the pipeline is successful, it will come as a green tick.

So…

Apart from that, this is the input file that we are taking from user. Here, currently, we are having a lot of input variables. This needs to be narrowed down based on NERF's requirement and whatever we want to give the user the control, whereas what we want is to keep the control, so this will change, but as of now, we have kept most of the things in the configurable.

So here, if you see, there is a variable called hosted versus the existing one. So hosted is, like, you have nothing, you don't have a pre-configured GitLab, you want to configure it from scratch, so it is hosted. Otherwise, if you have the existing GitLab, you can put it as existing and do the configurations accordingly.

Then, the project name I showed you, so this is the project name, like Omnia Catalog, you can give any other name. For each project, there is a visibility score that you can keep as private, public, and all of that.

Just a second.

So, then there are… Skipping stuff. It's okay.

Yeah. Then there are some ports

By default, we can keep the default values also. Otherwise, we can, like, reconfigure them to, let's say somebody has those ports, occupied, so we can change the codes, that is also configurable. Then we have also used, the GitLab, which is hosted, is a secure one, so it is HTTPS.

So, it can be both ways. It can be without the certificates also, and it can be with the certificates. The current flow which I have implemented is with the certificate.

So, on the background, we are creating our own certificates, and we are self-signing them. Later, if we want to change that approach, we can go ahead and, like, use a external certificate server, or whatever we want to do.

And based on the external flow, we can decide on how we want to keep the certificates. So, here is the path where the user can give, like, which is the directory where he wants to get the certificates installed. So, in case of external, they can just simply place it also here.

Then, the packages, like, which is the main, package for GitLab, we have also kept that, and currently, we have, like, validated with the latest app. Once we are finalizing the, like, requirements, we can keep it to a particular version and fix the versions. So, similar to that, we have some minimum requirement of hardware of that server, which should be documented, so it needs some

CPU cores, it needs some memory, and it needs some particular amount of hardware requirements, which we can come up and shortlist and document in our documentation.

And we have provided checks for it, but we have, like, given up random numbers as of now, like, which is the bare minimum working setup. So, apart from that, GitLab…

Ideally comes with a lot of services. There are, like, more than two databases, there are some monetary services, there are a few more workers, so all of that is also configurable. Some of those configurations I've mentioned here, and I've kept it to bare minimum. For example, we don't need

monitoring as of now. So, Prometheus and Grafana has been put to disabled, as of now, like, this is disabled, and the number of workers we have limited, then the concurrency also we have limited.

So all of that we have done.

Then, there is also input for, GitLab Runner, which is, like, which, which is the version. So, once we conclude on the version, we can come up with that version also, and move this latest to that particular version. So, all of these parameters are currently configurable, and we are taking as input.

Once we are done with our requirement, and we have everything finalized, you can

cut down from here and move it towards. So this is kind of the workflow. We have, like, come up with the basic workflow of how we want to integrate. We have the platform ready as…

So if I change the catalog production, it will rid of the runner? Yeah. And what does the runner execute?

The runner is kind of a podman container. Like, as of now, the pipeline definition is very basic. Now, currently, we have not written the stages, whatever this AP code, whatever, we have written the pass catalog, that one, that'll be invoked as part of that GitLab API. Yes, come.

So we have made a framework for currently hosted Git level, so we need to have a discussion, like, so there are a lot of input parameters, and actually, currently, we are not clear that

what all input parameter, nurse will give out of this. Because for nurse, it is like a…

external GitLab, we had to go. And… but we don't know, out of this parameter, are they going to give everything? Or… so that is something I think we want, maybe, to send the mail to nurse, asking, is this parameter you are going to give? Or… so that is, pending to conclude that part.

Okay. Huh. So they are able to confirm it.

Yeah, so we can share the…

Let's just share this input file to them, then we can get a confirmation of the deal.

Huh.

book. Thank you.

No, if you… internet is connected, you can…

Yeah, on my laptop, it is working, but the IPs are private, so we can use it in the RDP. So you can just use the playbook, give the inputs, and it will be working for your client.

100%.

Netri, I want to quickly finish addendum or not.

Definitely.

I don't.

Yep.

Amazing.

Takshi, if you… if it is there, you can start. I'll take it.

Sakshi Singla

Sakshi Singla

01:02:53

Sure, yes.

Please let me know once my screen is visible.

Abhishek S A

Abhishek S A

01:03:03

Yeah.

Sakshi Singla

Sakshi Singla

01:03:07

Okay, so,

I'll talk about LDMS telemetry, support when there is a slum node addition, user removes a slam node. So,

the…

technique that we have followed is we will track the Pixie mapping file changes, whether a user has, you know, made any change with respect to hostname, IP, or a slum node is added, or a slum node is removed.

So, we are comparing the checksums, of the files. So, when user runs the first discovery, right, initial discovery flow, we take a backup of pixie file and,

stored it under, telemetry directory. So, let's say now, user has, you know, removed one of the entry from Pixie mapping file. So, as you can see in the screenshots, the checksum of the original file will change, which I can compare with the backup file, which is stored inside telemetry.

to, you know, mark that change, basically. So, once it identifies that the file has changed, it will trigger the LDMS restart

But in that also, we have one check, which is,

to check whether the QBIP is actually reachable or not. In case the, you know, user runs Discovery again, and pixie file is changed, but the cluster has some issues. The QBIP, we are not able to SSH to it. Then it will display the message that it's not reachable, there might be some issues, and the LDMS pod restart will be skipped.

But we are mentioning the manual steps in this message, so that they can go to the control plane and do the steps by themselves, and it will not halt the, discovery flow execution. So this was, with respect to this only.

Sorry. Yes,

This is the ideal scenario when it is first discovery run, when restart of LDMS is not at all required, so it will skip it.

And we can see that it is pulling data from every node, first long control node, and 2 sl long nodes that I had in my cluster. Now, let's say one of the nodes, which is 34, we have removed from the,

pixie mapping file, then, it will trigger the LDMS restart configuration, from the playbook.

And on the cube control plane also, we can see that the 34 node was removed from the host mapping file, and then the LDMS config as well was updated with respect to it, and the pods also came up within, like, 10 to 20 seconds for the NASC LDMS aggregator.

And after this, when we ran, automated test for the LDMS, in that also, we can see that for the SLAM node 1, it is showing that, you know, it is, missing, no data is getting collected, but for this long control node and SLAM node, it is still proceeding, as before.

Now, coming to the other scenario, Slum Node Edition, we added the,

slum node part in Pixie file, ran the playbook again. Again, you can see that the node is coming back in the host map file for LDMS, and in the config file as well, it is listing the node for the data collection. And again, the pod came up very quickly after the restart, and the data was coming properly.

Abhishek S A

Abhishek S A

01:06:39

Okay, quick question. This pixie mapping file is generated, or it is handcrafted? Currently, manually, but, like, that's what Sujita was telling. From OIME, if we can generate, that is something we are looking at.

Yeah, no, met.

As you can see it. Ready?

He has shown, like, the output. Sakshi?

Sakshi Singla

Sakshi Singla

01:07:11

Yes, just a second.

Abhishek S A

Abhishek S A

01:07:12

Can you show me the screenshot where the metrics are…

Sakshi Singla

Sakshi Singla

01:07:20

Okay, so for… yeah, this is when everything is working fine, right? So I use the,

automated test run, like, which we have for LDMS… sorry, for telemetry, basically. So, for… it verify whether, whether all the pods were running or not, and then, the data that was getting collected from the SLAM.

Abhishek S A

Abhishek S A

01:07:45

When I remove a node, and I run the discovery elements, individual…

Right, to reprovision the all existing nodes. No, no, no, no, no, only that.

So it will remove it from the SLUM configuration. This is not slum, we are showing telemet.

Sakshi Singla

Sakshi Singla

01:08:04

LDMS, yeah, LDMS telemetry, basically.

Abhishek S A

Abhishek S A

01:08:07

telemetry part of the remote node. Actual…

ATMS is only supported for SLAM, okay, go ahead.

That day will come up, there is no…

Generator is still running, because the node is still alive.

Then what will happen? Will you have to bring error on that one?

Nordics remodeled.

We will not collect that data.

When slum nodes we are collecting on a service cluster. Slum nodes say LDMS data… Collecting the data in the service node cluster.

But before I turn off the NDMS and the iDirectory metering, I should have removed it from the Slurmstride. That they will take care. That is a separate epic that we are not showcasing now. So the sequence should be…

from a user's perspective, the way I will run this is, unless I have taken it out of Slurm, LDMS removal should not happen. Yes, yes, that they will… they are taking care of that. I mean, that is, I think infrastprint review was not there today, so in that, we'll cover that.

It's a together flow only, but she just showed another one part of the… I'm just trying to get the transaction correct. Okay. I suggested two different…

That's fun.

To cover the…

I'm just trying to understand the user's perspective of how they will experience this. Are you doing anything on that note?

Slam node only.

No, from that note, I'm just stopping you.

No, Aristotics are…

That's fine.

Best friend.

That can be done.

See, there's a scenario where the cluster is, like, we add the node to the live cluster, okay? Now, adding is a different scenario. You bring up everything and you add it, right? In the live node, you're silently deleting. The node is still… Yeah.

It becomes the augmented, you know, it'd be a big mess.

If there is a job running on it, and you go and mess with, like, this one, before you remove from Sclerm, I'm hoping it is going into a maintenance mode, and you let the job drain.

And it should have zero jobs pending on that one before you start pulling blood.

Yeah, that's the prerequisite. It's like I disturb the patient.

If he's on ventilator or whatever, doesn't matter, I will just discharge it first. Then I'll figure out whether I need to take the ventilator or not.

Can't be the case.

This rating is dead.

That's the feature, but am I implementing it before I pull it?

Okay.

Saying that what was the need to be removed.

You have to make sure there's no giant infection.

No, that's a documentation.

Question that they will explore it. I'll quickly finish on what I direct telemetry. This is for LDMS, same, like, LDRAC also, I mean.

But actually, yeah.

While adding to which circuit node I had it?

No, we are having only one port, no, LDMS is one only. No, no, LDMS is single.

either a natural can tell which pod you're adding.

They can't panic domain,

this, the, but the idea of the collection, and now we can demo the note.

from… for stopping the IDAC telemetry collection.

So, when I run telemetry.amline, like, you know, it means that the discovery flow itself, and the service cluster itself. After that, I'm running the telemetry.EAML.

If you see, this actually I tested on, VM cluster. If you see the IPs which are having a parent, right, that is all VMs.

Basically, it does not have proper IDRAC and all. So, it is based on our Pixi marking file, it has generated this.

Suppose when you… when you want to add a new node as part of discovery, some node.

The new node's IDRAC IP will get added into the BMC group data. When you add a remove, the new IDRAC copy will get added here. So, BMC data group, we will use it for telemetry add a review.

We will use this BRC data with the existing MySQL entries, and we'll compare, and we'll check whether any entries are getting added, or any entries are getting renewed. I mean, either the IPs are getting added to the telemetry collection, or anything getting removed from the telemetry collection.

If you see here, in this screenshot, I don't know whether you can see this… this screenshot, right? I have added two IPs, the proper IDRAC IPs, 132 and the 62,

And out of which, it started collecting the metrics for 132 and 62, because it was not able to enable the redfish command for collecting the telemetric.

it timed out, and we… we are collecting only the, for IDRAC IP-132, 7K2132. This is how the IDRAC technology report, and this is on the first run.

I'll… I'll show how, the second run, I can add two… two new IRAC IPs, that is 62 and 140. This one, which… which had timeout in the first run, and I'm trying to add these two IPs. And I… after adding them into the BMC,

BMCData.datagroup.cs, I ran the telemetric, and this is how, like, you know, my telemetry report is showing. It activated two IDRAC IPs.

When I checked in the telemetry, it is showing, along with the existing one, each and all the IDRA copies are getting added into the new, IDRA telemetry collection.

So, I… I verified, I ran a consumer script.

You know, which was already there. So, for the new IDRAPITCHA, the IDRAPs, we started getting the metrics.

And for the other mode as well.

Ready to participate, then?

In the mapping file. Mapping file, mapping. Yeah, let's discuss on that part. It should get added to the correct essaylet, because there is a need for…

Every… every compute node can be addressed to every assembly, right? Actually, based on parent, we are one parent, we are assigning one first.

No, I don't you have to say…

So, each track has got its own… I'll be exact.

The more you have added to UTO would act on interactive.

So, in each essay, did I have the correct LinkedIn, Those respective acts.

So, currently, each board is having its own parent.

One folder has their own parent. So that parent to port mapping is there.

We are mapping internally that. Yeah.

But you're looking at the subject? Pardon?

Subnet, we are reacting and multi-subnet, but… Mapping is already there.

Yeah, okay.

When the user adds into the mapping file, the BMC… when we run discovery.ramml, bmcdatagroup.csv will get updated, and from the BMC data group, when we run telemetry.ramml, either it will start collecting or it will disable them.

For the add node I covered, for the remove node.

So, here…

I want to remove, IDRAC IP71.62 from the IDRAC telemetry Collection. If you see, like, you know, in the activated list, it is showing both 62 and 140, and even here, it is showing, it's a

But actually, later I… No, no, this is the report she's telling. We'll not… we don't need to give an input. This is the report… Users just need to…

You will remove that pixie mapping file.

You can see the number… I added a demo based on the piximabic, right?

So, here I'm showing the report, where it is showing the IP font which got removed from the telemetry, and also the IDRAC IPs.

When I checked, actually, the report, I actually disabled and left it for some time. Then I went back to report and checked when was this last collected for this iTrack IP. I ran it on Feb 14, and I checked on Feb 16th, so it was all showing for this,

remote IP was showing only for, like, you know, if you see the time, right, when I convert it, the transaction…

Do not stop correcting.

No disability.

Node is remote, but yes, once user runs telemet.tlement, they normally will stop typing.

That is, only for iDride telemetry, there is a playbook separately that we told, right? For hydride telemet.

You can pay credit to Mavicia Skidra.

automated this,

adding, and running the add or remove processes, right? We should be tying it to the lab actions.

If you get the disturbed from the whole store that file on the GitLab.

You have it triggered. There's an upgrade.

Of the re-electing to either delete or the edition.

Who triggered on these kids.

In Cuban or Kyoto.

Steed by pizza.

QNR. Because if I say QN or Q2, you'd say which CR.

Mr.

He was not… he wouldn't want to go.

For removing the slum nodes, we can only add and remove slump nodes. For removing the slump node, you have… user need to run discovery or damage. Then.

He has to come see for stopping by the user assistance. This is one economic transaction.

If I'm removing an old, if I'm moving out of an apartment.

I walked all with my stuff.

Right? I'll leave my friend.

I take only one clothes, no.

And it is there. What I'm saying is, we don't want to keep the…

my task-level details to be operated again and again. We need to have that workflow kind of a thing. Ideally, in the GitLab kind of way, that's why we are investing in getting the GitLab there.

Right? So we need to think our solution to be more and more automated than having to do that. Those questions of, okay, functionality asked, you took it out of Slurm.

But you're collecting the dog, and if somebody else is using that for something else, then this…

disconnect, right? So, I think we need to really think through how whatever investments we have be connected seamlessly and not depend on manual interventions as much as possible.

So here, for disabling the direct value, we are not restarting the Ubernetes board.

he got remote at his recommendation to them. He's still functioning. All services are working. It's not good enough.

You could start very slow, and end with cleanup fucking graphics.

Yep.

Ideally, if OAMA is present, it should start there. If not, I will edit the IP list in the GitLab.

And that kicks off a runner, which will take this step in the… put it in maintenance mode, wait for it to drain the jobs, then clean up whatever jobs are there, remove access to that floor.

follow on. Are you moving from OpenCheme assembly also now? Right? That is getting removed.

Open stuff.

Then there is a very clean way to run that. You should update with email alert.

One. So, next time, you will not even be able to book. So, that is proper renewable. All services are proper. Whenever it's reboot, again, for it.

Mix everything is reboot.

You have to just put it, but…

restarting the continuous state pool set. We are just disabling the right push command to stop collecting the telemetry, and we are renewing from the MySQL entries. Awesome.

I direct pending it to receive it.

All right, nope.

For the ad node, we are restarting. For new node, you need to restart it. So that it will collect new, but if already transmitter is not sending the data, it will not collect it, right? Collector won't collect it, so we don't need to restart, so that we can save the data loss.

What did we have to cover, but briefly?

APA. All that APA floor. Not all the APA? Not all. Build image you are targeting.

I didn't fail.

I mean, from the last one, additional 4.7 are done.

3 we had already done last time.

3n plus 4.

For… for… Oh, they said 3. Now, pass catalog, generate input, local rep will build image 4.

This… this… I think.

That is next to the next question is the best description.

We'll have a meeting tomorrow based on Anna is a great one-hour discussion. I really am behind on…

point out, yeah, he's jumping out. I really want to catch up on that.

