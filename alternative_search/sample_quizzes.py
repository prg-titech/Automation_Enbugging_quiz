###
text1 = '''def cons(x:Int,list:List[Int]): List[Int] = {
    x :: list
}'''

ans_change1 = ((50,51),'true')

ans_error_msg1 = '''Found:    (true : Boolean)
Required: Int'''

editable_places1 = [(20,29),(32,41),(50,51),(55,59)]

error_place1 = (50,54)

quiz1 = (text1,ans_change1,ans_error_msg1,editable_places1,error_place1)

###
text2 = '''case class Color(red: Int,green: Int,blue: Int)

def revColor(c: Color): Color = {
    c match{
        case Color(r,g,b) => Color(255-r,255-g,255-b)
    }
}'''

ans_change2 = ((131,148),'255-r,255-g')

ans_error_msg2 = '''missing argument for parameter blue of method apply in object Color: (red: Int, green: Int, blue: Int): test.Color'''

editable_places2 = [(43,46),(73,78),(115,120),(131,148)]

error_place2 = (125,143)

quiz2 = (text2,ans_change2,ans_error_msg2,editable_places2,error_place2)

###
text3 = '''def head(l1: List[Int]): Int = {
    l1 match{
        case Nil => 0
        case x::xs => x
    }
}'''

ans_change3 = ((60,63),'_')

ans_error_msg3 = '''Unreachable case'''

editable_places3 = [(25,28),(60,63),(67,68),(85,87),(91,92)]

error_place3 = (80,85)

quiz3 = (text3,ans_change3,ans_error_msg3,editable_places3,error_place3)

###
text4 = '''def makepairs(l1: List[Int],l2: List[Int]): List[(Int,Int)] = {
    (l1,l2) match {
        case (Nil,_) => Nil
        case (_,Nil) => Nil
        case (x1::x1s,x2::x2s) => (x1,x2)::makepairs(x1s,x2s)
    }
}'''

ans_change4 = ((97,104),'(Nil,Nil)')

ans_error_msg4 = '''match may not be exhaustive.

It would fail on pattern case: (Nil, List(_, _*))'''

editable_places4 = [(18,27),(97,104),(108,111),(125,132),(136,139),(162,169),(174,181)]

error_place4 = (68,75)

quiz4 = (text4,ans_change4,ans_error_msg4,editable_places4,error_place4)

###
text5 = '''def ifprint(x:Int)(y:Boolean): Int = {
    if(y) println(x)
    x
}

def use_print(x:Int): Int = {
    ifprint(x)(true)
}'''

ans_change5 = ((113,119),'')

ans_error_msg5 = '''Found: Boolean => Int
Required: Int'''

editable_places5 = [(49,59),(110,113),(113,119)]

error_place5 = (103,113)

quiz5 = (text5,ans_change5,ans_error_msg5,editable_places5,error_place5)

###
text6 = '''def greater[A](x: Int,y: Int): Boolean = {
    x > y
}'''

ans_change6 = ((25,28),'A')

ans_error_msg6 = '''None of the overloaded alternatives of method > in class Int with types
    (x: Double): Boolean
    (x: Float): Boolean
    (x: Long): Boolean
    (x: Int): Boolean
    (x: Char): Boolean
    (x: Short): Boolean
    (x: Byte): Boolean
match arguments ((y : A))'''

editable_places6 = [(12,13),(18,21),(25,28),(31,38)]

error_place6 = (45,48)

quiz6 = (text6,ans_change6,ans_error_msg6,editable_places6,error_place6)

###
text7 = '''def not(x: Boolean): Boolean = {
    if (x == true) false
    else true
}'''

ans_change7 = ((62,66),'')

ans_error_msg7 = ''' A pure expression does nothing in statement position; you may be omitting necessary parentheses'''

editable_places7 = [(52,57),(62,66),(67,71)]

error_place7 = (52,57)

quiz7 = (text7,ans_change7,ans_error_msg7,editable_places7,error_place7)

###
text8 = '''def numbering(list: List[String]): List[(String, Int)] = {
    def subnum(list: List[String], pos: Int): List[(String, Int)] = {
        list match {
            case Nil => Nil
            case x :: xs => (x, pos) :: subnum(xs, pos + 1)
        }
    }
    subnum(list, 0)
}'''

ans_change8 = ((258,273),'')

ans_error_msg8 = '''Found: Unit
Required: List[(String, Int)]'''

editable_places8 = [(20,32),(35,54),(167,170),(258,273)]

error_place8 = (258,259)

quiz8 = (text8,ans_change8,ans_error_msg8,editable_places8,error_place8)