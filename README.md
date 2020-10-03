# donut-buddies

This Python program randomly pairs up members of a Facebook group and posts the pairings (or "donut buddies") to the Facebook group according to user's inputs. Possible uses include: generating hangout groups, mentor/mentee pairings, and more. Facebook login and group information required. This program requires an upload of a CSV file with a one or two-column list of names. 

## To Run: 
1. Clone this repository
2. Navigate to your cloned repository
```
$ cd /path/to/directory/
```
3. Download the dependencies
```
$ pip install -r requirements.txt
```
4. Run the script and provide your Facebook login and group link to the popup interface. 
*Make sure your CSV files are a one or two-column list of names, with two columns representing distinct groups across which to pair members. For two-column CSV files, ensure that the first column is the longer list of names. Examples files are provided in the repository.*
```
$ python donut.py
```

## To Do: 
- [ ] Add option to automatically schedule posts
- [ ] Improve exception handling
- [ ] Use Facebook API to automatically pull group information and members
- [ ] Pairing of odd number of members
