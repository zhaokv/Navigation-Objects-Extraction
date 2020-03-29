The original data can be download here: 
1. CleanEval: http://cleaneval.sigwac.org.uk
2. SSD: http://cogcomp.cs.illinois.edu/Data/MSS/

We label each page manually as follows: 
1. A new artificial attribute "cluster" is added to each hyperlink. "cluster=nav" means it belongs to a navigation object, and "cluster=other" otherwise. 
2. Hyperlinks belongs to the same cluster are labeled by the same "clusterindex", e.g. "clusterindex=0".
3. The navigation objects are classified into three categories: 
  - The Navigation Bar is labeled as class="naviBar"
  - The Navigation List is labeled as class="naviList"
  - The Navigation Location is labeled as class="naviLoc"