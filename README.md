# Cupertino Forum Application Bot

This bot is used by the Cupertino Forum to automate the application intake and voting process.

A Zapier automation is triggered when an application is submitted to the official google form. It takes the information from the submission and formats the responses into a google doc using a template. It then sends the command this bot is listening for into the applications channel of the Cupertino Forum discord server, passing applicant state name and discord username as parameters. This bot will then be triggered to grant the applicant role to the discord username provided in the application, open a thread under the applications channel for discussion with the same name as the applicant state, post a reaction role vote in the applications channel exactly 48 hours later, then 24 hours later it will announce the result and either grant or not grant the membership role to the applicant based on the number of aye/nay reactions.

All role IDs and tokens have been redacted from the bot code.
