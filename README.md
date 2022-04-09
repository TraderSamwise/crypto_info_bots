Original repo which has the Elon AI model etc: https://github.com/PiotrRut/elonmusk-twitter-notifier

## Prerequisites 🗂

In order to run this locally, make sure you're Python interpreter is between v3.6 and 3.8 - 
this is due to the fact that Tensorflow won't work with newer versions. If you're on a newer
Python version, consider downgrading with [pyenv](https://github.com/pyenv/pyenv).

To install all the necessary dependencies, simply run the following command inside project root 👇🏻

```bash
$ pip install -r requirements.txt
```

Note:
I have *not* included my trained AI model in the repository due to the large file size - 
you can get it by navigating to the [releases](https://github.com/PiotrRut/elonmusk-twitter-notifier/releases) tab, downloading `doge-ai.h5` and placing it in the root
of the project.

## Install ##

`pip install -r requirements.txt`
copy `.env_template` to `.env` and fill in the desired `.env` vars

## Twitter Developer Account

If you would like to use this yourself, and receive juicy e-mail notifications every time
Elon tweets, you can too! All you have to do is to have a [Twitter Developer account](https://developer.twitter.com/en) and update the environmental variables with your credentials

## Accounts to follow

You can configure the `src/constants.py` file directly to specify what twitter accounts to follow. `src/tweet_engine_dispatcher.py` is used to choose which handler to use when a new tweet comes in so you can handle different tweets from different accounts with different actions.

## Production Docker ##

Install Docker and Docker Compose. https://docs.docker.com/compose/
Make sure `docker-compose.yml` file has `.env` vars correctly configured.
Then from the base dir run `docker-compose up`

## Customization ##

If you don't need all functionality (like pushing to discord) you may have to dig into the code and disable any usage of related `.env` vars. This project wasn't intended for public use and it hasn't been designed well for configurability 


USE AT YOUR OWN RISK. NOT FINANCIAL ADVICE.
