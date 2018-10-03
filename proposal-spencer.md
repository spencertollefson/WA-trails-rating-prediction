Spencer Tollefson

October 3, 2018

Proposal for Project Benson

#   Predict hiking trail rating on wta.org

The [Washington Trail Association](https://wta.org) is a non-profit advocacy group that focuses efforts on promoting hiking in the state of Washington. The organization, beginning as *Signpost* magazine in 1966, currently pursues goals including reducing barriers to hiking, volunteer trail maintenance, organizing hiking activities, encouraging people to access the outdoors, and providing information to the public.

WTA has created and provided, free-of-charge, a database of over 3,500 hikes in Washington state. These hikes differ from short strolls to multi-day backpacking extravaganzas. The database web GUI allows visitors to filter from the list of all hikes by selecting from over 30 features, such as location, length, mountain views, beaches, and more. Additionally, visitors may write a "trip report", essentially a forum comment, and rate each hike on a 5-star scale.

Each "hike" has its own web page which displays all hike features in an aesthetically pleasing manner, as well as a hike description, directions to the trail, and Google Map view.

[Here is an example page](https://www.wta.org/go-hiking/hikes/wilderness-peak)

## Question/Need:

Predict the rating (on a 0-5 scale) of any hike give its set of features.

This prediction model, while mostly for my fun and learning, could potentially help WTA and other trail authorities decide which features to invest in when maintaining or creating new trails.

## Description of data:

Each hike can contain up to 30 features. Included are a number of continuous features, such as the length of the hike or number of trip reports. Additionally, about half of the features are binary-categorical features. They indicate the presence of something like a "coast" on a hike, and is indicated as present or not present.

For some pages, there is extensive information on the authority responsible for maintaining the trail head or on the author of the website description. Because of this I have made multiple fields (author 1, author 2) to capture this information for pages in which it exists. It will fill as None for pages it does not exist.

![jupyter notebook sample](https://raw.githubusercontent.com/spencertollefson/WA-trails-rating-prediction/master/src/common/images/example-wta-df.png "Sample of one row of data")

Each hike page contains the following features.

features
- name
- region
- subregion
- total votes
- rating
- length (miles)
- length is one-way or round trip
- gain (feet)
- highest point (feet)
- parking/entrance fee
- latitude
- longitude
- trailhead information 1
- trailhead information 2
- author 1
- author 2
- count of trip reports

binary categorical features
(These features are either present or not on the hike)
- Wildflowers/Meadows
- Ridges/passes
- Wildlife
- Waterfalls
- Old growth
- Summits
- Good for kids
- Dogs allowed on leash
- Fall foliage
- Lakes
- Rivers
- Coast
- Mountain views
- Established campsites


## Characteristics of each row of data:

Each row of data will be a record for a particular hike. There are currently 3,555 hikes in the database according to the WTA website. Thus I expect that many rows, with a field for each of the features listed above.
