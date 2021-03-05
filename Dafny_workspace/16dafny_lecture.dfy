datatype Exp = Const(int) | Plus(Exp, Exp)

function eval(e:Exp) : int {
    match e
    case Const(n) => n
    case Plus(e1, e2) => eval(e1) + eval(e2)
}

datatype Instr = Push(int) | Add
datatype List<T> = Nil | Cons(T, List<T>)

function run(program:List<Instr>, stack:List<int>) : List <int>
{
    match program
    case Nil => stack
    case Cons(instr, k) => // k is 'continuation', or rest of program
        match instr
        case Push(n) => run(k, Cons(n, stack)) // push the thing to the stack and run the rest of the program
        case Add     =>
            match stack
            case Cons(n, Cons(m, stack')) => run( k, Cons((n+m), stack') )// n is top, m is second, stack' is the rest of stack
            case Nil => Nil // return Nil stack to indicate error
            case Cons(n , Nil) => Nil // we are also accessing m so m must not be Nil as well

}