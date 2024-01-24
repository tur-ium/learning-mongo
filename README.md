Learning Mongo
==============
Repository for active learning while studying document-orientated database system *MongoDB*

# Setup
1. Install MongoDB (if not done already)
2. Sign up for OpenWeather API access 
3. Create conda project
```commandline
conda create -n mongo_env --file environment.yml
```
4. Create a `.env` file by copying `.env.template` and placing your Open Weather API key in the corresponding line

# Usage 
```commandline
python main.py
```

# Contributing
- Don't share your .env file (its in the .gitignore for a reason!)
- Update requirements using:
```conda env export > environment.yml```
