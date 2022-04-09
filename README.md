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

## Twitter Developer Account 👨🏻‍💻

If you would like to use this yourself, and receive juicy e-mail notifications every time
Elon tweets, you can too! All you have to do is to have a [Twitter Developer account](https://developer.twitter.com/en) and update the following environmental variables with your
Twitter API access keys:


