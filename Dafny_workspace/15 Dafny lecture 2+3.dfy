datatype List<T> = Nil | Cons(T,List<T>)

datatype Tree<T> = Leaf | Node(T,Tree<T>,Tree<T>)

function length<T>(xs:List<T>) : int
ensures length(xs) >= 0
ensures xs == Nil ==> length(xs) == 0
// does not work. ensures length(append(xs,ys)) == length(xs) + length(ys)
{
    match xs
        case Nil => 0
        case Cons(x,xs') =>  1+length(xs')
}

// length(Nil)         == 0
// length(Cons(x,xs')) == 1+length(xs')

function append<T>(xs:List<T>, ys:List<T>) : List<T> 
ensures xs == Nil ==> append(xs,ys) == ys
ensures ys == Nil ==> append(xs,ys) == xs
// ensures length(append(xs,ys)) == length(xs) + length(ys)
{
    match xs    
        case Nil => ys
        case Cons(x,xs') => Cons(x,append(xs',ys))
}
// append(Cons(x,xs'),ys) == Cons(x,append(xs',ys))

// a * (b + c) = a*b + a*c
// length(append(xs,ys)) = length(xs) + length(ys)
// axiom:  length(Cons(x,xs')) == 1+length(xs')

method emma<T>(xs:List<T>, ys:List<T>)
ensures length<T>(append(xs,ys)) == length<T>(xs) + length(ys)
// Lemma: forall xs:List<T>, ys:List<T> . length(append(xs,ys)) == length(xs) + length(ys)
{
    match xs
    case Nil => { /*
        assert    length(append(Nil,ys))
               == length(ys)
               == 0 + length(ys)
               == length<T>(Nil) + length(ys)
               == length(xs)  + length(ys)
               ; */
    }
    case Cons(x,xs') => {
        emma(xs',ys);  // get postcondition length(append(xs',ys)) == length(xs') + length(ys)
     /* assert     length(append(xs,ys))
                == length(append(Cons(x,xs'),ys))
                == length(Cons(x,append(xs',ys)))
                == 1 + length(append(xs',ys))
                == 1 + length(xs')     + length(ys)
                == length(Cons(x,xs')) + length(ys)
                == length(xs)          + length(ys)
                ; */

    }
}

// 1+(2+3) == (1+2)+3
// append(Cons(x,xs'),ys) == Cons(x,append(xs',ys))

method appendAssoc<T>(xs:List<T>, ys:List<T>,zs:List<T>)
ensures append(xs,append(ys,zs)) == append(append(xs,ys),zs)
{
    match xs
        case Nil => {}
        case Cons(x,xs') => {
            appendAssoc(xs',ys,zs); // PC: append(xs',append(ys,zs)) == append(append(xs',ys),zs)
          /*  assert append(xs,append(ys,zs))
                == append(Cons(x,xs'),append(ys,zs))
                == Cons(x, append(xs',append(ys,zs)))
                == Cons(x, append(append(xs',ys),zs))
                == append(Cons(x, append(xs',ys)),zs)
                == append( append(Cons(x,xs'), ys), zs)
                == append( append(   xs,       ys), zs)
                
                ;*/
        }
}

// dafny lecture 3 starts here

function member<T>(x:T, ys:List<T>) : bool 
decreases ys
ensures ys == Nil ==> member(x,ys) == false
{
    match ys
    case Nil => false
    case Cons(y,ys') => x==y || member(x,ys')
}

// (1) member(x,Cons(y,ys')) == (x==y || member(x,ys'))
// (2) append(Cons(x,xs'),ys) == Cons(x,append(xs',ys))

method lemmaMemberAppend<T>(x:T,ys:List<T>,zs:List<T>) 
ensures member(x,append(ys,zs)) == (member(x,ys) || member(x,zs))
{
    match ys
    case Nil => {}
    case Cons(y,ys') => {
        // (3) ys == Cons(y,ys')
        lemmaMemberAppend(x, ys', zs);
        // (4) some variant of member(x,append(ys,zs)) == (member(x,ys) || member(x,zs))
        assert member(x,append(ys,zs))
            == member(x, append(Cons(y, ys'), zs))        // (3)
            == member(x, Cons(y, append(ys', zs)))        // (2)
            == (x==y || member(x, append(ys', zs)))       // (1)
            == (x==y || member(x,ys') || member(x,zs))    // (4)
            == (member(x, Cons(y, ys')) || member(x, zs)) // (1) (backwards)
            == (member(x,ys) || member(x,zs))             // (3)
            ;

    }
}