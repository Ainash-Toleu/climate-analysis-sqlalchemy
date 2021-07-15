# Climate Analysis SQLAlchemy 

## Step 1 - Climate Analysis and Exploration

* Tables into SQLAlchemy ORM reflected

* Exploratory Precipitation Analysis were done

* Exploratory Station Analysis were done

* Results were plotted using Matplotlib

![pic1](Images/pic1.png)

![pic2](Images/pic2.png)

## Step 2 - Climate App

After completing initial analysis, Flask API was designed to create following routes:

* `/`

  * Home page.

  * All routes that are available listed.
  ![pic3](Images/pic3.png)

* `/api/v1.0/precipitation`

  * The query results to a dictionary using `date` as the key and `prcp` as the value converted.

  * The JSON representation of a dictionary returned.
  ![pic4](Images/pic4.png)

* `/api/v1.0/stations`

  * The JSON list of stations from the dataset returned.
  ![pic5](Images/pic5.png)

* `/api/v1.0/tobs`
  * The dates and temperature observations of the most active station for the last year of data queried. 

  * The JSON list of temperature observations (TOBS) for the previous year returned.
  ![pic6](Images/pic6.png)

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * The JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range returned.

  * When given the start only, `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date calculated.
  ![pic8](Images/pic8.png)

  * When given the start and the end date, the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive calculated.
  ![pic7](Images/pic7.png)
