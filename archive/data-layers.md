# Data Layers

As mentioned in the  overview we have separated our data into different layers to help see how it progresses through the system. While we primarrily expet connsumerrs to acces data fromt he consumerr  layer therre may  be reasons  why they  need to access data from other layers too. Especially  if it can reduce the processing time. It's worth noting  that providers and managers will also need visibility of data in all layers.

### Stocks Vs Flows
A lot of our  data can eithe be considered one oft he following:

* a stock - something that we have to keep historically and cannot be recreated through processing. It is very important that we do not lose this as there  won't be a way to  recreate it from other data. When  alterinng code be weary of this!
* a flow - a piece of data that is created from a stock  or anotherr flow. At any given time 

### Raw Data Layer



