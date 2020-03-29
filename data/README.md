The original data can be downloaded here: 
1. CleanEval: http://cleaneval.sigwac.org.uk
2. SSD: http://cogcomp.cs.illinois.edu/Data/MSS/

We sample a part of data and label each page manually as follows: 
1. A new artificial attribute "cluster" is added to each hyperlink. "cluster=nav" means it belongs to a navigation object, and "cluster=other" otherwise. 
2. Hyperlinks belong to the same cluster are labeled by the same "clusterindex", e.g. "clusterindex=0".
3. The navigation objects are classified into three categories: 
   - Navigation Bar: labeled by class="naviBar"
   - Navigation List: labeled by class="naviList"
   - Navigation Location: labeled by class="naviLoc"
