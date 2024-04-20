<h1 align='center' style="text-align:center; font-weight:bold; font-size:2.5em"> Media Company Website (with data base)</h1>

<p align='center' style="text-align:center;font-size:1em;">
  

![](https://github.com/its-Raz/Media-Company-Website/blob/master/presentation/order_return.gif)
</p>





# Contents

- [Overiew](#Overiew)
- [Setup](#Setup)


# Overview


|                     <h5 align='center' style="text-align:center; font-weight:bold; font-size:2.5em"> Home Page</h5>                            | 
| :------------------------------------------------------ | 
|         <img src="./presentation/home.JPG" width="100%">   |

|                     <h5 align='center' style="text-align:center; font-weight:bold; font-size:2.5em"> Queries Page</h5>                            | 
| :------------------------------------------------------ | 
|         <img src="./presentation/query.JPG" width="100%">   |
|This page retrive the newest queries result from the data base.
you can find the full specifications for each query [HERE](https://github.com/its-Raz/Media-Company-Website/blob/master/presentation/queries_spec.JPG)|


|                     <h5 align='center' style="text-align:center; font-weight:bold; font-size:2.5em"> Records Mangament Page</h5>                            | 
| :------------------------------------------------------ | 
|         <img src="./presentation/record.JPG" width="100%">   |
|This page outlines three parts:
1. Recording Order:
- Users input the family name and desired program in a form, with a submission button.
- Error message appears if family identifier doesn't exist.
- Records requests are rejected under various conditions.
- Error message displayed if request isn't approved, listing the reason(s).
- If approved, update RecordOrders scheme.
2. Recording Return:
- Similar form to recording order, but for returning recordings.
- Error messages displayed if program doesn't exist or isn't owned by the family.
- If return is approved, update RecordOrders (remove the order) and RecordReturns (add returned recording) relationships.
3. Recording Query Documentation:
- Additionally, a table displays the top three families based on the highest total number of programs ordered and the number of programs they have ordered, sorted in descending order by the number of programs ordered.|
  
# Full-Specifications
**Full-Specifications**

 
 # Setup
**Setup**

1. Clone this repository and 

   ```bash
   git clone https://github.com/its-Raz/ds-algs.git
   
   ```
2. Run ```Test.java```
3. Compare ```my_output.txt``` to ```test_output.txt```
# Full-Specifications
**Full-Specifications**
 [([ds_algs_specs.pdf](https://github.com/its-Raz/ds-algs/blob/master/ds_algs_spec.pdf))]
