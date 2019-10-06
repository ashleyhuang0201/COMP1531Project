# Iteration 2 Plan

In iteration 2, we will begin by developing authentication functions. In order to develop other functions, we must first have users that are able to log in and interact with slackr. We estimate that this will take us 4 days. Next we will develop the functions required for creating and maintaining of channels. Channels are required to send messages. We estimate this will take around a week. Once users are able to use channels, we will implement functions used for the sending and interaction of messages in these channels, we will allocate half a week to implement these tasks. Quality of life functions such editing profile are implemented last after the basic slackr functions are implemented. This will take us half a week.

Authentication will require us to handle a database of emails and passwords so people will be able to log in once they have registered. The email and password will need to be associated with the respective user information, possibly through the use of a dictionary. When a user logs in, a token will have to be generated. This generation of a token will require a hash. A database of tokens is required for other functions to check that the function is being called by a valid user.  

Channels will require us to handle a database of currently active channels. When given a channel id, it will need to check that the channel id corresponds to an active channel The functions will need a method of verifying the token of the user, possibly through comparing it with a list of currently active tokens.

Messages will require us to have a database of all messages posted in the channel. The message should be stored with a message id so they can be checked to be valid messages as well as being searchable.

Quality of life functions will require checking the token is valid and then using the database of tokens to identify who the user is.

In order to ensure our project is progressing on time, we will be meeting in person every Thursday for group checkup, discussion and any further enquiries relating to the project. Documentation will be completed on a Google Doc and GitLab so members can constantly edit and view the latest version of the document. We plan to use multiple branches in the development stage to have an effective git workflow.

During the next stage of development, we will improve on our current software development practices such as effective git workflow. By utilising multiple branches in GitLab, we can ensure the code in the main branch is always functional. Many functions are interdependent and thus by also maintaining a working version, multiple dependent functions can be worked on simultaneously with minimal conflict.

Constant communication is ensured through Facebook Messenger and Discord. Scheduled online calls can be conducted to solve any major issues that required all members' opinions.We will have standups on Tuesday and Friday (in person or via call) and weekly recaps on Sunday. Peer programming through screen share on discord to allowed us to peer program when not in the same location.

![alt-text](https://i.imgur.com/QynYJhy.png)
