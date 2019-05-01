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

LIST
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

```
