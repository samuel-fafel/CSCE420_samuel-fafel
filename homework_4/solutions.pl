% Samuel Fafel - 330003077
% CSCE420-500
% ------------- Q1 Simpsons -------------
% Parent definitions
parent(bart,homer).
parent(bart,marge).
parent(lisa,homer).
parent(lisa,marge).
parent(maggie,homer).
parent(maggie,marge).
parent(homer,abraham).
parent(herb,abraham).
parent(tod,ned).
parent(rod,ned).
parent(marge,jackie).
parent(patty,jackie).
parent(selma,jackie).

% Gender definitions
male(bart).
male(homer).
male(herb).
male(burns).
male(smithers).
male(tod).
male(rod).
male(ned).
male(abraham).

female(maggie).
female(lisa).
female(marge).
female(patty).
female(selma).
female(jackie).

% Kinship rules
brother(X, Y) :- 
    male(Y), 
    parent(X, Z), 
    parent(Y, Z),
    X \= Y.

sister(X, Y) :- 
    female(Y), 
    parent(X, Z), 
    parent(Y, Z),
    X \= Y.

aunt(X, Y) :-
    parent(X, Z),
    sister(Z, Y).

uncle(X, Y) :-
    parent(X, Z),
    brother(Z, Y).

grandfather(X, Y) :-
    male(Y),
    parent(X, Z),
    parent(Z, Y).

granddaughter(X, Y) :-
    female(Y),
    parent(Z, X),
    parent(Y, Z).

ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :-
    parent(X, Z),
    ancestor(Z, Y).
% ------------- Q1 Simpsons -------------

% ------------- Q2 Queries -------------
% Occupations
occupation(joe,oral_surgeon).
occupation(sam,patent_lawyer).
occupation(bill,trial_lawyer).
occupation(cindy,investment_banker).
occupation(joan,civil_lawyer).
occupation(len,plastic_surgeon).
occupation(lance,heart_surgeon).
occupation(frank,brain_surgeon).
occupation(charlie,plastic_surgeon).
occupation(lisa,oral_surgeon).

% Addresses
address(joe,houston).
address(sam,pittsburgh).
address(bill,dallas).
address(cindy,omaha).
address(joan,chicago).
address(len,college_station).
address(lance,los_angeles).
address(frank,dallas).
address(charlie,houston).
address(lisa,san_antonio).

% Salaries
salary(joe,50000).
salary(sam,150000).
salary(bill,200000).
salary(cindy,140000).
salary(joan,80000).
salary(len,70000).
salary(lance,650000).
salary(frank,85000).
salary(charlie,120000).
salary(lisa,190000).

% Helper rules to define occupations
lawyer(trial_lawyer).
lawyer(patent_lawyer).
lawyer(civil_lawyer).
surgeon(oral_surgeon).
surgeon(plastic_surgeon).
surgeon(heart_surgeon).
surgeon(brain_surgeon).

% Helper rules to define cities
california(los_angeles).
texas(houston).
texas(dallas).
texas(san_antonio).
texas(college_station).

% Query2a: Find all lawyers
query2a(X) :- 
    occupation(X, Y),
    lawyer(Y).

% Query2b: Find all surgeons who live in California
query2b(X) :- 
    occupation(X, Y),
    surgeon(Y),
    address(X, Z),
    california(Z).

% Query2c: Find all surgeons who live in Texas and make over $100,000/yr
query2c(X) :- 
    occupation(X, Y),
    surgeon(Y),
    address(X, Z),
    texas(Z),
    salary(X, S),
    S > 100000.

% ------------- Q2 Queries -------------

% ------------- Q3 CanTeach -------------
% Database of facts
subject(algebra,math).
subject(calculus,math).
subject(dynamics,physics).
subject(electromagnetism,physics).
subject(nuclear,physics).
subject(organic,chemistry).
subject(inorganic,chemistry).

degree(bill,phd,chemistry).
degree(john,bs,math).
degree(chuck,ms,physics).
degree(susan,phd,math).

retired(bill).

% Predicate to define if someone can teach a subject
canTeach(X, Y) :-
    subject(Y, Z),
    degree(X, phd, Z).

% Predicate modification to exclude retired people
canTeach2(X, Y) :-
    subject(Y, Z),
    degree(X, phd, Z),
    not(retired(X)).

% Predicate modification to allow people with a PhD or an MS and not retired
canTeach3(X, Y) :-
    subject(Y, Z),
    degree(X, DegreeLevel, Z),
    (DegreeLevel = phd; DegreeLevel = ms),
    not(retired(X)).
% ------------- Q3 CanTeach -------------

% ------------- Q4 Octal Codes -------------
% Define a bit.
bit(0).
bit(1).

% Define the octal_code predicate.
octal_code(A, B, C) :-
    bit(A),
    bit(B),
    bit(C),
    format("~w~w~w~n", [A, B, C]).

% ------------- Q4 Octal Codes -------------

% ------------- Q5 Map Coloring -------------
% Define the possible colors.
color(red).
color(green).
color(blue).

% Define the mapcolor predicate with inequality constraints.
mapcolor(WA, NT, SA, Q, NSW, V, T) :-
    color(WA),
    color(NT),  WA \= NT,
    color(SA),  WA \= SA,   NT \= SA,
    color(Q),   NT \= Q,    SA \= Q,
    color(NSW), SA \= NSW,  Q \= NSW,
    color(V),   SA \= V,    NSW \= V,
    color(T).
% ------------- Q5 Map Coloring -------------
