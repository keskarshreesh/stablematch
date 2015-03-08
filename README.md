# stablematch
Stable Matching Algorithm for the Hospital-Residents Problem

The Hospital-Resident problem involves finding stable matches between residents (doctors) and hospitals. This program uses an extended version of the Gale-Shapley algorithm, originally developed by Rob Irving[1].

#To build
```
gnatmake src/solve_hr.adb
```

#To generate sample data
```
python data/generate_preflists.py
```

#To run
```
./solve_hr < data.txt
```

#Input
Input is given as text on standard input as follows:
- Line 1: N, M, positive integers, numbers of residents and hospitals respectively
- Lines 2..N+1: the resident preference lists, each has form X : A B C ...
- Lines N+2..M+N+1: the hospital preference lists, each has form X : P : A B C ..., where P is the number of positions available

Sample data can be generated using the script *generate_preflists.py* in the *data* folder.

#Output
Output is given as a list of matched pairs in the form (Resident,Hospital) saved to file as *output_ro* (resident-optimal) and *output_ho* (hospital-optimal).

#References
1. Dan Gusfield & Robert W. Irving, The Stable Marriage Problem: Structure and Algorithms (MIT Press)
