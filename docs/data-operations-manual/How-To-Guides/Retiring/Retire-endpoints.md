
## Retiring individual endpoints

1. **Find the endpoint/source(s) to be retired**  
     
   Use the following [link](https://datasette.planning.data.gov.uk/digital-land/reporting_latest_endpoints?_sort=rowid&collection__exact=brownfield-land&organisation__exact=local-authority-eng%3ACAB) to list the endpoints of a particular organisation and dataset. The example lists Cambridge City Council brownfield-land endpoints. If we get a new endpoint, make note of the endpoint hash of the old one.  
     
2. **Retire endpoint/source(s)**  
     
   Retiring an endpoint and the associated source(s) is pretty straightforward. All you need to do is find the endpoint/source(s) in their respective files (*endpoint/source.csv*), via the `endpoint` hash, and add an `end-date` in the format `YYYY-MM-DD`.There may be multiple sources for one endpoint so be sure to retire all of them.   
   
## Retiring a batch of endpoints

**Data monitoring:**

We might have a data monitoring ticket which aims to retire all erroring endpoints. We have a handy sql query which identifies all the endpoints we have deemed to be retired based on some criterias. The query for this can be found [here](https://datasette.planning.data.gov.uk/digital-land?sql=WITH+unique_endpoints+AS+%28%0D%0A++SELECT%0D%0A++++collection%2C%0D%0A++++pipeline+as+dataset%2C%0D%0A++++endpoint%2C%0D%0A++++organisation%2C%0D%0A++++name%2C%0D%0A++++MIN%28endpoint_entry_date%29+AS+endpoint_entry_date%0D%0A++FROM%0D%0A++++reporting_historic_endpoints%0D%0A++WHERE%0D%0A++++%28%0D%0A++++++%22endpoint_end_date%22+is+null%0D%0A++++++OR+%22endpoint_end_date%22+%3D+%22%22%0D%0A++++%29%0D%0A++++AND+%22endpoint_entry_date%22+%3C+DATE%28%27now%27%2C+%27-1+year%27%29%0D%0A++++AND+%22status%22+NOT+LIKE+%222%25%22%0D%0A++GROUP+BY%0D%0A++++collection%2C%0D%0A++++endpoint%2C%0D%0A++++name%0D%0A%29%2C%0D%0Alatest_log_entry+AS+%28%0D%0A++SELECT%0D%0A++++endpoint%2C%0D%0A++++MAX%28latest_log_entry_date%29+AS+latest_200_log_entry_date%0D%0A++FROM%0D%0A++++reporting_historic_endpoints%0D%0A++WHERE%0D%0A++++status+%3D+%27200%27%0D%0A++GROUP+BY%0D%0A++++endpoint%0D%0A%29%0D%0ASELECT%0D%0Aue.collection%2C%0D%0A++ue.dataset%2C%0D%0A++ue.name%2C%0D%0A++p.project%2C%0D%0A++p.provision_reason%2C%0D%0A++ue.endpoint%2C%0D%0A++strftime%28%27%25d-%25m-%25Y%27%2C+ue.endpoint_entry_date%29+as+endpoint_entry_date%2C%0D%0A++strftime%28%27%25d-%25m-%25Y%27%2C+l.latest_200_log_entry_date%29+as+latest_200_log_entry_date%2C%0D%0A++CAST%28%0D%0A++++julianday%28%27now%27%29+-+julianday%28l.latest_200_log_entry_date%29+AS+int64%0D%0A++%29+as+n_days_since_last_200%2C%0D%0A++s.source%0D%0AFROM%0D%0A++unique_endpoints+ue%0D%0A++LEFT+JOIN+source+s+ON+ue.endpoint+%3D+s.endpoint%0D%0A++LEFT+JOIN+latest_log_entry+l+ON+ue.endpoint+%3D+l.endpoint%0D%0A++LEFT+JOIN+provision+p+on+ue.dataset+%3D+p.dataset%0D%0A++and+ue.organisation+%3D+p.organisation%0D%0AWHERE%0D%0A++%28%0D%0A++++l.latest_200_log_entry_date+%3C+DATE%28%27now%27%2C+%27-5+day%27%29%0D%0A++++OR+l.latest_200_log_entry_date+IS+NULL%0D%0A++%29%0D%0A++AND+%22n_days_since_last_200%22+%3E+90%0D%0AORDER+BY%0D%0A++ue.dataset%2C%0D%0A++julianday%28%27now%27%29+-+julianday%28l.latest_200_log_entry_date%29+desc) (currently it is returning erroring endpoints which have been erroring for more than 90 days e.g. where `n_days_since_last_200 > 90`. The easiest way to do this is to retire the endpoints as a batch.

1. **Query all erroring endpoint:**  
   Copy the csv output of the query.

2. **Paste into retire.csv:**  
   If you do not already have `retire.csv`, create it in the root folder. Then paste the csv data copied from step 1 into that csv file (easiest way to do this is paste in in VSC).  
     
3. **Run retire\_endpoints\_and\_sources**  
     
   Run the following command. For this example, the location of `retire.csv` is in the root of config.  
 


```
digital-land retire-endpoints-and-sources retire.csv
```

4. **Check the results**  
   Double check if all the endpoints and sources that are meant to be retired have an end-date added to the corresponding line. There should be as many endpoints retired as given in retire.csv. There should be at least the same amount of retired sources (remember that multiple sources can be associated with an endpoint)
