### quick Guide

### 1- overview


![overview](https://github.com/keffadi/The-tuto/blob/master/python_django/django1.jpg)

### 2- Python

integer = 23    
Floating point number = 23.000    
string = 'hello'   ```#  "hello" / myvar = "j'ai mange"  / myvar = 'j\'ai mange' ```


in Terminal
```
python
print ("hello world")
exit()
```
Some commandes
```
print (2+1)    # ("string")  (number)
my_var = 10
myVar = 20
total = my_var + myVar
print(total)
```
```
total = 'abcde'
print(total[0])
output: a

total = 'abcde'
print(total[1:])
output: bcde

total = 'abcde'
print(total[:1])
output: a

total = 'abcde'
print(total[1:3])
output: bc

[1:] FROM position 1 is included in output  / [:1] UP TO position 1 is not included in output

total = 'abcdef'
print(total[::2])
output: ace  # write first index, then jump second index, write third, then jump fourth ........
total = 'abcdef'
print(total[::3])
output: ad   # write, jump, jump, write, jump, jump
```
Upper, Lower, Capitalize, split
```
total = 'abcdef'
new_var = total.upper()
print(new_var)
output: ABCDEF

total = 'hello world'
new_var = total.split()
print(new_var)
output: ['hello', 'world']

total = 'hello world'
new_var = total.split('o')
print(new_var)
output: ['hell', ' w', 'rld']


upper can be: lower, split, replace ...........
```
insert another string in string
```
total = 'insert another string here : {}'.format('hello world')
print(total)
output: insert another string here : hello world

total = 'insert another first string here : {}, then second word here {}'.format('hello world', 'hello NaN')
print(total)
output: insert another first string here : hello world, then second word here hello NaN

total = 'insert another first string here : {b}, then second word here {a}'.format(a='hello world', b='hello NaN')
print(total)
output: insert another first string here : hello NaN, then second word here hello world

```

LISTs
```
mylist = [3,'ok',34,'une patate',[1,2,3]]
print(mylist)
output: [3, 'ok', 34, 'une patate', [1, 2, 3]]`

print(len(list))
output: 5

print(mylist[1])
output: ok

print(mylist[-1])
output: [1, 2, 3]

mylist = [3,'ok',34,'une patate',[1,2,3]]
mylist[-1] = 'keffadi'
print(mylist)
output: [3, 'ok', 34, 'une patate', 'keffadi']

mylist.append('new item')
print(mylist)
output: [3, 'ok', 34, 'une patate', [1, 2, 3], 'new item']

mylist.extend(['a','b','c'])     # ['a','b','c'] can be myOtherlistVar, extend include list content to list, defferent of append
print(mylist)
output: [3, 'ok', 34, 'une patate', [1, 2, 3], 'a', 'b', 'c']

mylist = [3,'ok',34,'une patate',[1,2,3]]
itempoped = mylist.pop()
print(mylist)
print(itempoped)
output:[3, 'ok', 34, 'une patate']
output:[1, 2, 3]

mylist = [3,'ok',34,'une patate',[1,2,3]]
mylist.reverse()
print(mylist)
output: [[1, 2, 3], 'une patate', 34, 'ok', 3]

mylist = [3,7,30,24,23,5,5,8]
mylist.sort()
print(mylist)
output: [3, 5, 5, 7, 8, 23, 24, 30]

mylist = [3,'ok',34,'une patate',[1,2,3]]
print(mylist[-1][0])
output: 1

matrix = [[1,2,3],[4,5,6],[7,8,9]]
first_col = [row[0] for row in matrix]
print(first_col)
output: [1, 4, 7]


```

DICTIONARIEs
```
myDict = {"01_Mai":"Mercredi","02_Mai":"jeudi","03_Mai":"Vendredi","key4":2020}
print(myDict)
output: {'01_Mai': 'Mercredi', '02_Mai': 'jeudi', '03_Mai': 'Vendredi','key4':2020}

print(myDict["01_Mai"])
output: Mercredi

myDict = {"01_Mai":"Mercredi","02_Mai":"jeudi","03_Mai":"Vendredi","key4":{123:[1,2,'jesuisla']}}
print(myDict["key4"][123][2])
output:jesuisla

print(myDict["key4"][123][2].upper())
output: JESUISLA

myDict[01_Mai] = "ANY"  # can be use to update a value or add "key":"value"

```

TUPLEs, SETs and BOOLEANs
```
my_tuple = (1, "ok", "olivier")  # is immutable, can't be modify
thisset = {"apple", "banana", "cherry"}    #You cant access items in a set by referring to an index, ''unordered''. bracket as Dict, take unique element, cant take two same item
Boolean are just true or false

my_tuple = (1, "ok", "olivier")
print(my_tuple[2])
outpot:olivier

mySet = set()
mySet.add('keffa')
mySet.add('malouda')
print(mySet)
output: {'malouda', 'keffa'}

converted list to set  
converted = set([1,1,1,2,2,3,4])
print(converted)
output: {1, 2, 3, 4}


```

Control flow
```
if 1<2:
    print("yes!")
elif 1==2:
    print("Equal")
else:
    print("Noo!")
output: yes!

# here the blockote {} is recognized by indentation, and python use :  as ;

# Loop
seq = [1,2,3,4,2,9,10]    # for seq = {"dicti":1}, the output will be the key dicti and ''unordered''
for item in seq:
    print(item)
output: 1
2
3.....   

seq = {"01_Mai":"Mercredi","02_Mai":"jeudi","03_Mai":"Vendredi","key4":2020}
for item in seq:
    print(item)
    print(seq['01_Mai'])
output: 01_Mai
Mercredi
02_Mai ......

 

```


