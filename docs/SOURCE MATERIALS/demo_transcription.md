Transcript
26 February 2026, 11:33am

Ds, Vasanth started transcription

Sa, Abhishek   0:03
Yeah this is the path. So under this path there are two files. So there is there is a playbook folder and Sibel play. I'm bringing in your chat also.

Ds, Vasanth   0:11
Mhm.

Sa, Abhishek   0:17
That also.

Ds, Vasanth   0:18
OK.
OK.

Sa, Abhishek   0:19
Download it for a fresh install.
Then.
You can see my chat also, right?

Ds, Vasanth   0:33
Yeah, I can.

Sa, Abhishek   0:35
Linux.

Ds, Vasanth   0:38
OK.

Sa, Abhishek   0:40
We're good to know, yeah.
OK, so.

Ds, Vasanth   0:45
This is the path and then you have collaboration.

Sa, Abhishek   0:48
So the the there are two playbook. Huh. The first step is that I don't need to give now. I mean if you can let you know.

Ds, Vasanth   0:56
Yeah.

Sa, Abhishek   0:58
OK, so now after this right user can run the. So there is some input file for GitLab config. OK for now there are many input. OK, out of many input there are some input are still under discussion. OK, but for now what you can do?

Ds, Vasanth   1:05
Hmm.
OK.

Sa, Abhishek   1:14
You can come up with this many input variable and you come up with the initial input variable. You can update it because the discussion is going on OK.

Ds, Vasanth   1:20
Hmm.
OK.

Sa, Abhishek   1:24
So that will be.

Ds, Vasanth   1:31
Like.

Sa, Abhishek   1:31
Oh.
So Vasant, you can this variable you can update. OK, once again I'm pinging you.

Ds, Vasanth   1:39
Hmm.

Sa, Abhishek   1:43
Yeah, can you in this one right? GitLab host is the IP of the target. I mean you know that remote node wherever the unit to deploy GitLab. OK and this is the server server host IP.

Ds, Vasanth   1:45
Hmm.
OK.
Hmm, node in the sense of the server, is it?
Let's type OK.

Sa, Abhishek   2:00
And this is the project name.

Ds, Vasanth   2:03
Oh.

Sa, Abhishek   2:04
This is the private or public and this is the main branch.
This much you keep it and remaining variable. I'll come and explain if something. For now let us keep this one and this will be present in GitLab console.yaml.

Ds, Vasanth   2:09
OK.
Huh.
OK.
OK, so why they want to select private or public to private is default is something there. So what?

Sa, Abhishek   2:25
Uh, see, it is basically I'll show, I'll show you, I'll show you. You know our is for public or private.

Ds, Vasanth   2:28
Uh.
Public.

Sa, Abhishek   2:33
So this is like a build. I mean there like there is a gitlab. The gitlab repo can be public or private. It is same like that basically. So check if you see here this I'll just show you.

Ds, Vasanth   2:38
Hmm.
Huh.
OK.
Hmm.

Sa, Abhishek   2:49
One sample 1234.
So this is 1 project. OK, this is the GitLab we are instance you are creating. See this is the Omnia catalog. This is what you are seeing. The project name you saw in that input file here. OK so that project we created and also.

Ds, Vasanth   3:03
Hmm.
OK, yeah. Um.
OK.
Hmm.

Sa, Abhishek   3:17
Here we have the if you can see here private there is a log button to identify it's private and see the main branch.

Ds, Vasanth   3:25
Hmm.
OK.

Sa, Abhishek   3:30
See, just I think that GitLab is same as GitHub. It's another thing. Basically you think Omnia is deploying, I mean GitLab. It's like same as Omnia is deploying GitHub. GitLab is another company like GitHub which does the same thing.

Ds, Vasanth   3:36
OK.
Uh huh. OK.

Sa, Abhishek   3:47
You got it right. It's also one source management source control system where you can keep your code and everything. There also will have the branches project directory like the same thing like here you think root is the in our case root is Dell.

Ds, Vasanth   3:48
Got it.
Hmm.
OK.
Hmm.

Sa, Abhishek   4:04
And Omnia here it is root Omnia catalog.

Ds, Vasanth   4:07
OK.

Sa, Abhishek   4:09
What idea, right? I mean, any doubt?

Ds, Vasanth   4:10
Yeah, yeah, got it, got it. So do the do the customer has to set it as private or public? Their choice, OK.

Sa, Abhishek   4:17
That is use their choice now.
Yeah.
OK then Omnia Gitlab. This is fine. This is something and here by default Omnia creates a catalog file.

Ds, Vasanth   4:28
Hmm.
OK, so when it will create it when the run this playbook is it?
Uh.

Sa, Abhishek   4:40
Of Omnia.

Ds, Vasanth   4:42
Now you have we have we have chosen the IP address and selected whether it's private or public and then we we have given the value for the project name and then how then when this will get created running a playbook is it?

Sa, Abhishek   4:49
Mm.
So that gitlab.yaml right? So the gitlab.yaml playbook whatever I show now. So this playbook will install the GitLab on the server. So the GitLab will be installed on this that particular server and it will set up the GitLab instance here. This will be a GitLab instance which is.

Ds, Vasanth   5:04
Oh.
Uh.
OK.
OK.

Sa, Abhishek   5:20
Running and in this GitLab instance, it'll so it'll upload a GitLab CA file and a catalog file.

Ds, Vasanth   5:20
Hmm.
OK, OK.

Sa, Abhishek   5:28
And you heard about this catalog in our demo, correct? Yeah, I mean they would have heard it correct. So this is this is the catalog file where you will have customer fill will fill all their package details where like this here like there are different section function layer and this different package layer. So what I'm thinking.

Ds, Vasanth   5:31
Could I correct correct?
Hmm.
Huh.
Hmm.

Sa, Abhishek   5:48
In your examples you can give the catalog. So I'll give you a sample catalog. OK, I don't know how can we give that in the example. I don't know because it's too big, right? It's like 4000 lines of file. I don't know we can keep this in the example file.

Ds, Vasanth   5:54
OK.
Hmm.
Mhm.
Yeah, they need to automate. It seems updating catalog file itself. They need to automate.

Sa, Abhishek   6:06
So actually so we have a script. So even I'll tell you there is a script to to generate this catalog also that also I'll tell you. OK, so basically there will be a catalog file and there is a pipeline file. This is we we are in work in progress, OK.

Ds, Vasanth   6:12
Oh.
OK.
OK.

Sa, Abhishek   6:23
So this is the pipeline file. In this pipeline file you will have you will invoke. I mean you would have heard about our APF invocation right? Like I mean you heard our demo they were showing on last time so and they were running on Python script that time you remember if you remember I mean it was going in a CLA way.

Ds, Vasanth   6:25
Hmm.
Hmm.
Uh.
Right.
Hmm.

Sa, Abhishek   6:42
So basically you you know we have our so you know after prepare OEM we so we need to add this GitLab install installation after prepare OEM.

Ds, Vasanth   6:43
Right. Uh.
Hmm.
Hmm.
OK.

Sa, Abhishek   6:55
OK, so after prepare AM, the server will run the gitlab.yaml OK and it will install this gitlab and everything and from on actually normally after prepare AM the next step is local repo.

Ds, Vasanth   6:58
Hmm.
OK.
Hmm.

Sa, Abhishek   7:08
Correct. Now user doesn't not need to run the local repo.

Ds, Vasanth   7:09
Correct.
Oh.

Sa, Abhishek   7:14
User doesn't not need to run the local repo. Why? Because that local repo will be triggered from here in the pipeline. Basically if you wanted to know see if you see here there is a create local repo.

Ds, Vasanth   7:18
Hmm.
This OK, OK.
Mhm, mhm.

Sa, Abhishek   7:29
Just for your understanding, this is all our different stages or something. It's a pipeline code. Basically whatever the remaining playbook after prepare OM local repo build image discovery right? I mean those are the Omnia flow flow right? These playbooks will be invoked from the GitLab pipeline.

Ds, Vasanth   7:30
Uh, yeah.
Mm.
Uh uh.
Right.
Hmm. OK.

Sa, Abhishek   7:49
That that is what is happening.

Ds, Vasanth   7:52
Understood.

Sa, Abhishek   7:54
You got it right instead of your manually triggering this one from the.

Ds, Vasanth   7:55
Huh.

Sa, Abhishek   8:00
This CLA you can run a pipeline so that pipeline will be triggered based on the softwares defined in the and you know our softwares are defined currently in software configuration. Now user can give whatever the software details, everything what they wanted in so catalog.

Ds, Vasanth   8:01
Running uh.
OK.
Uh.
OK.

Sa, Abhishek   8:17
So based on the catalog which has all the softwares, it will trigger the pipeline and it will start the local repo and like build image and discovery and it will install OS on all the nodes. Then that's it that that is it. I mean I'm.

Ds, Vasanth   8:19
Hmm.
Hmm.
OK.
Hmm.
OK.
Uh.

Sa, Abhishek   8:32
Coming to a minimal level just to give overall idea for you how what is build stream so.

Ds, Vasanth   8:36
OK.
OK, so let me reiterate the entire workflow.

Sa, Abhishek   8:43
Yeah, sure.

Ds, Vasanth   8:43
So then you correct me if I'm wrong. So first assume that I'm a customer and what I would do is I will first of all go ahead and update the buildstream config YAML file that I enabled the buildstream configuration.

Sa, Abhishek   8:46
Oh.
Yes, correct.

Ds, Vasanth   9:00
That would be the first part, right? And then what they would do is they run in YAML's file, they run the prepare OAM so that it it creates a container, build stream container in the OAM.

Sa, Abhishek   9:02
Oh.
Mm.
Correct says once this is enabled it will create the build stream container and it will create the Postgres containers also.

Ds, Vasanth   9:15
Uh.
OK, why? OK, so why do we need a Postgres container to store?

Sa, Abhishek   9:20
Yeah, I mean, yeah.
Uh, for storing for storing the transaction details of this API calls.

Ds, Vasanth   9:31
OK. So should the customer should aware of it?

Sa, Abhishek   9:35
Our customer will be we need in in the Omnia target right? You need to update the Omnia target that currently that under Omnia target there are different services right? That Omnia target you need to update. So under Omnia target we will have additionally Omnia build stream container.

Ds, Vasanth   9:38
Uh.
Uh.
OK.
Hmm.

Sa, Abhishek   9:50
Uh then uh playbook watcher service and and Postgres.

Ds, Vasanth   9:52
Was.

Sa, Abhishek   10:09
Yes, they'll run this get level.

Ds, Vasanth   10:12
So it's kind of preparing the GitLab pipeline, so it creates a pipeline and also the catalog file will be placed here.

Sa, Abhishek   10:15
Uh, yes, yes.
Now it will create the project so the gitlab.yaml will create the project and pipeline both. So now this is the pipeline, the builder so so they can go to this project to go to. There is a build pipeline. If they go to pipeline you will see the pipeline also.

Ds, Vasanth   10:23
Oh.
OK uh.
Uh.
So how much the customer should aware of this pipeline? Should we need to document anything about the pipeline?

Sa, Abhishek   10:38
OK.
No, they can tell. But see what is currently we are planning is user has to go to the.

Ds, Vasanth   10:46
Huh.
Get low.

Sa, Abhishek   10:50
Now code, code, code repository. User will go to the code repository. I mean code and repository section. Under code repository there will be GitLab CA and catalog. So what user has to do? This is the default catalog. By default there will be a catalog available that is the default Omnia template.

Ds, Vasanth   10:51
Oh.
OK.
Hmm.
Hmm.
Uh.
Hmm.

Sa, Abhishek   11:08
If you serve one, you can make a change of this catalog. So based on every catalog change, consider you modify this file, catalog file and automatically the pipeline will be triggered.

Ds, Vasanth   11:09
OK.
Hmm.
Uh.
OK, so if I modify and push the changes, is it or just something like when I modify?

Sa, Abhishek   11:24
See consider you now. Now you're making Omnia doc change right in your GitHub. Similarly you if you made a change, you will commit it, right?

Ds, Vasanth   11:29
Uh.
That it? Uh.

Sa, Abhishek   11:33
Same here. If you made a change and commit here, it will trigger the pipeline automatically.

Ds, Vasanth   11:38
OK, so then it.

Sa, Abhishek   11:40
The bit.
Based on a catalog change like consider. Basically I'm telling now this is the catalog. I'll go and edit it.

Ds, Vasanth   11:45
Oh.
Hmm. OK.

Sa, Abhishek   11:51
And I'll change it to the version to 1.034. I mean I'm changing to just to something then it will basically it will trigger the pipeline.

Ds, Vasanth   11:55
Huh.
OK. So when it triggers the pipeline or after triggering the pipeline, what would be the customer action? Is it something like you will keep on monitoring the pipeline?

Sa, Abhishek   12:08
No customer has to. Ha, yes. Now they can go to build and go to pipelines or jobs. They can go to the jobs where all the jobs are running.

Ds, Vasanth   12:16
Oh, OK.
OK.

Sa, Abhishek   12:19
So now the pipeline is triggered and like here you can go to pipelines also. So now you can go to this. This is the pipeline, right? This is the pipeline and pipeline has. This is the change and you can see this is the different stages of pipeline. See one passed, 2 passed. So this is the pipeline you can click here.

Ds, Vasanth   12:22
Mm.
Hmm.
OK.
Hmm.
Uh.
OK.

Sa, Abhishek   12:38
And you'll see that this stage. If you go to stages, you can go to the stage details also if you want what happened in each stage if if you go to job.

Ds, Vasanth   12:41
Mm.
Hmm.
OK, the green. Yeah, good.

Sa, Abhishek   12:51
Green tech is means it is past.

Ds, Vasanth   12:54
Mm.

Sa, Abhishek   12:55
Hmm.

Ds, Vasanth   12:56
OK, So what if it fails in the between? What customer is supposed to do? That's an bug.

Sa, Abhishek   13:00
Customer has to no no. He has to go and check the what is the error here. Now it's something it failed so there should be error and based on the error user has to take the action.

Ds, Vasanth   13:11
OK, so that would be a separate troubleshooting section, right?

Sa, Abhishek   13:16
That should be a yeah, yeah, that's yes that that's why you would have seen I am. I have created some troubleshooting stories to you. Let's say like I I don't know like that Rajesh and Priti has to give you whatever troubleshooting address that they have to give you.

Ds, Vasanth   13:16
Is that or any?
Hmm.
OK, OK, understood. OK, so then he will monitor it and then a customer will monitor it and everything is success at the back end, the discovery job will run.

Sa, Abhishek   13:31
Yeah.
So the now this pipeline, now this pipeline will come. See now this is this pipeline has consider 7 stages. All the seven stages will become successful. Then only the overall status will become successful. Consider there are now here. I mean it is work in progress. That's why you are seeing.

Ds, Vasanth   13:48
Oh.
OK.
Hmm.

Sa, Abhishek   13:58
There are 7 stages means it will show us 7 stages successful. So now this last stage is failed. That's why it is showing failed. Consider. I'll show you consider see this is a one stage with only one stage so and see you can see as a past.

Ds, Vasanth   13:58
Hmm.
OK.
Hmm.
Hmm.
OK, hmm, correct.

Sa, Abhishek   14:15
Correct.
Basically like that. So based on the overall job stage, this is the stages, this is the overall, this is the overall status and this is the individual stage status. Individual stages you can think of like a local repo, build image, discovery, I mean authentication, registration, those are the individual stages.

Ds, Vasanth   14:19
Hmm.
Hmm.
Hmm.

Sa, Abhishek   14:35
I mean individual playbook execution is kind the kind of something is individual stages.

Ds, Vasanth   14:35
OK.
Understood. OK, so once it is success, the final stage is all the all the pipeline is success and then that means it it would have discovered all the devices and deployed OS packages and everything on the nodes, right?

Sa, Abhishek   14:50
Uh, the.
Uh.
Correct, correct, correct, yes.

Ds, Vasanth   15:00
How would they verify it? Or do they need to verify manual?

Sa, Abhishek   15:02
Manually that is manually for for for now it is manually OS that will automate again we will enhance currently that discovery. Currently if you see discovery only there no after discovery we don't have a mechanism to automate it that we are in work in progress for now they have to manually verify.

Ds, Vasanth   15:07
OK.
Um.
Uh.
OK.

Sa, Abhishek   15:21
Oh.

Ds, Vasanth   15:22
So, and they were also talking about this thing, right? The testbed, testbed, they'll deploy it on a testbed and then they will promote it. That is.

Sa, Abhishek   15:30
So that we are not doing now that we are not doing now that we'll whatever the mapping file is, see how it will be like it is. Basically we have our input file in the provision config mapping file, same mapping file, it will read and it will fix the boot.

Ds, Vasanth   15:34
Uh, no test bed just directly.
OK.
Mhm.
Oh.
OK.
OK, Abhishek. And what else? I've got an idea.

Sa, Abhishek   15:53
You got idea?
And one more thing, there is something called in settings. In settings there is something called CACD. Under CACD there is something called runners. So this is the this is the runner which is helping to run the pipeline. So so we need to tell this runner will be online always so we can see.

Ds, Vasanth   16:02
Hmm.
Hmm.
OK.
Hmm.

Sa, Abhishek   16:18
There is a project that see you think as one. OK, you think like this like so GitHub is a project right? I mean or Dell Omnia so that is that is installed but pipeline is a separate thing. I mean correct.

Ds, Vasanth   16:20
Hmm.
Oh.
Hmm.

Sa, Abhishek   16:33
Pipeline is separate. So for in order to run a pipeline and it's some something called runner. Runner is nothing but a a portman container like you can see like build stream one container is there right like that I just for your understanding I'll just show you.

Ds, Vasanth   16:34
Right.
Hmm.
OK.
Oh.
There's a container running on GitLob.

Sa, Abhishek   16:50
Uh.
Correct. Yes, correct. Yes. So you can see pod man PS. This is the runner. This is like a GitLab runner. Got it right?

Ds, Vasanth   16:55
OK.
OK, So what is the difference between this runner and in the GitLab project you have 3 files there along with the catalog chairs and what is the other one? How do you name it? Can you go to the GitLab? Can you go to the GitLab project?

Sa, Abhishek   17:19
Which one?
Oh.

Ds, Vasanth   17:26
Uh, project.

Sa, Abhishek   17:28
Project term.

Ds, Vasanth   17:29
Oh.

Sa, Abhishek   17:31
Oh.

Ds, Vasanth   17:33
So that's the runner. What is this one? GitLab CI dot YAML.

Sa, Abhishek   17:35
Mm.
Now this is the file. This is the file for the pipeline. What? What should be the pipeline? Content of the pipeline? How many stages? Like how to define now? What is the stages required for the pipeline so that define the pipeline definition is part of this here.

Ds, Vasanth   17:39
The first one, uh.
Huh.
OK.
Mm.
OK.
Huh.

Sa, Abhishek   17:55
This file has the pipeline definition. What should be run when you trigger a pipeline?

Ds, Vasanth   18:00
OK, so this pipeline will be then. OK, it runs this pipeline in the container, right in the GitLab container.

Sa, Abhishek   18:13
And.

Ds, Vasanth   18:14
That's my understanding, right? You have this file which has the definition when the pipeline is triggered.

Sa, Abhishek   18:16
Yes, yes. When it will it when that trigger the pipeline, it will run in this container. Yes, correct.

Ds, Vasanth   18:24
OK.

Sa, Abhishek   18:24
Yes, yeah.
It is the execution environment. This render means the execution environment for this pipeline.

Ds, Vasanth   18:32
OK.

Sa, Abhishek   18:33
Yeah, correct.

Ds, Vasanth   18:35
Under.

Sa, Abhishek   18:38
Can you come up with the initial draft then we can discuss further?

Ds, Vasanth   18:40
Sure, sure. And just one more thing. So this request is a separate section, right? Means this would be.

Sa, Abhishek   18:48
After prepare OEM you can. After prepare OEM you can add it.

Ds, Vasanth   18:53
OK, because it's like a uh, it's a different.

Sa, Abhishek   18:54
And you can keep it as option after prepare OEM.

Ds, Vasanth   18:59
Yeah, sorry, sorry, go ahead complete.

Sa, Abhishek   19:01
After prepare OM we need to add this and now one doubt I have is like currently here there is one flow. OK now prepare OM build stream. So I wanted to know build stream flows can we should we have separately that we need I need alignment from the we need to check or should it be?

Ds, Vasanth   19:05
Hmm.
Uh.
Hmm.
Hmm.
OK.

Sa, Abhishek   19:21
Part of like see now when build stream is enabled, the user doesn't need to run this one local rep or something correct that end their documentation need to remember. That is what I was thinking now.

Ds, Vasanth   19:23
Hmm.
No, what I would suggest is because at least not two different customers would be using. It could be the same customer would be using the existing workflow, the same customer would be using the build stream workflow, but.

Sa, Abhishek   19:49
Correct.

Ds, Vasanth   19:50
It has two different flows. Their objective is different, right? So in that case I I was thinking about having a separate section called build stream, automate with build stream or deploy.

Sa, Abhishek   19:56
Mhm.
Where from here? From where you will have from here.

Ds, Vasanth   20:06
Yeah.
So you have Omnia deployment guide, right? Outside of Omnia deployment guide, we'll have a section called Build Stream, Automate with Build Stream or Orchestrate with provision with.

Sa, Abhishek   20:12
Oh.
That is fine, but in that case that yeah, that also good. In that case we need to some of the section in order to duplicate it.

Ds, Vasanth   20:22
Mm.
And referent.
Uh, I think that should be fine, I think.

Sa, Abhishek   20:30
Or a refer it. Either you should duplicate or you can have a reference of the file.

Ds, Vasanth   20:31
Mm-hmm. Yeah.

Sa, Abhishek   20:35
If that can be done, it'll it'll be good.

Ds, Vasanth   20:37
Mm-hmm.

Sa, Abhishek   20:39
Because it will be confusing.

Ds, Vasanth   20:39
Yeah, I'll think about it. Uh.

Sa, Abhishek   20:44
Correct other.

Ds, Vasanth   20:44
Definitely I don't want to merge it with the existing workflow because their objective would be different.

Sa, Abhishek   20:50
Character.

Ds, Vasanth   20:51
Every time you would add up if condition. If you are using build stream, build stream process you do this.

Sa, Abhishek   20:55
We'll stream how do the it will come. Yeah, maybe I think good. Maybe you come up with a initial one, then we can check because you need to check with Vengard also. Maybe you come up with the initial one and we can check with Vengard and Ravi.

Ds, Vasanth   21:04
Yeah, sure. Hmm.
OK.
OK, sure thing by end of day tomorrow that I.

Sa, Abhishek   21:13
OK.
OK, fine. Yeah, yeah, you'll come. You'll come up with a top level directory change, right?

Ds, Vasanth   21:18
OK.
Oh, yeah.

Sa, Abhishek   21:23
OK. Thank you. Yeah.

Ds, Vasanth   21:28
When you say top level directory, you're saying the workflow.

Sa, Abhishek   21:28
Thanks.
Uh yes, at least till till GitLab. I'm not expecting till full till GitLab.

Ds, Vasanth   21:32
Oh.
Uh huh.
OK. And can you share this project with me, the one that you're running? I'm not gonna change anything. I'll just see. Is that positive?

Sa, Abhishek   21:45
No, that is used by. It is used by Rajesh. I mean, if something happen, it'll be a problem. I'll I'll try to deploy one more instance and try to give you.

Ds, Vasanth   21:48
Like this.
OK, actually the screenshot would work.

Sa, Abhishek   21:58
That you can check the recording, right? It'll be in recording. OK. OK. Thanks.

Ds, Vasanth   22:00
Yeah, right. OK.

Ds, Vasanth stopped transcription
