# Referral system
The referral system is a tool used by many commercial companies operating on the Internet. 
The referral program allows you to motivate customers to invite people 
from their environment to participate in commercial relations with the company. 
In a successfully designed program, all participants receive their material benefits: 
referrers of the program can be rewarded with a percentage of the funds spent by their referrals 
on the company's products or services or with a fixed fee, 
referrals receive welcome gifts or increased discounts on the company's products, 
the company receives profitable advertising and loyal new customers.

## Referral system with API website
This repository contains a website project that implements the functionality of the referral program 
through the interface on Django templates and through the API. 
The project is written on the Django and Django REST frameworks and consists of two dynamic pages: 
user authorization, user profile 
and several API views that process user requests 
for authorization in the referral system, 
getting a list of user referrals, 
getting own invite code and determining the referrer of an authorized user.

## Why was this project written
This project is an implementation of a test task from Hammer Systems. 
All the main requirements of the technical assignment were fulfilled in the project. 
In addition to TA, there have been added styles to Django templates.

Working on this project allowed me to develop a custom user manager and custom user model, design and code user registration and authorization via SMS codes, and develop an API using the Django REST framework.

## Implementation
- [Technical assignment](https://www.iliasamodin.ru/media/for_external/hammer_systems/pdf/%D0%A2%D0%B5%D1%81%D1%82%D0%BE%D0%B2%D0%BE%D0%B5%20%D0%B7%D0%B0%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%B4%D0%BB%D1%8F%20Python%20%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%87%D0%B8%D0%BA%D0%B0%20%E2%80%94%20Hammer%20Systems.pdf)
- [Hosted website](https://iliasamodin.pythonanywhere.com)
- [API instructions](https://iliasamodin.pythonanywhere.com/?section=Instruction)