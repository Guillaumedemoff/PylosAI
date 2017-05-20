#Player 1
#random ((0,1,1),(0,2,1),(0,2,1),(0,2,2)) sur un des 4 au centre


#Player 2
#random ((0,1,1),(0,2,1),(0,2,1),(0,2,2)) il ne pourra pas jouer là où le joueur 1 aura mis sa 1ère boule logiquement


#Player 1 case 1
#if P1 in (0,1,1) and P2 in (0,1,2)
    #random((0,2,0),(0,3,0),(0,3,1))

#if P1 in (0,1,1) and P2 in (0,2,1)
    #random((0,0,2),(0,0,3),(0,1,3))

#if P1 in (0,1,1) and P2 in (0,2,2)
    #random((0,2,0),(0,3,0),(0,3,1),(0,0,2),(0,0,3),(0,1,3))

#Player 2 case 1
#if P1 in (0,1,1) and P2 in (0,1,2) and P1 in ((0,2,0) or (0,3,0) or (0,3,1))
    #random((0,3,2),(0,3,3),(0,2,3))

#if P1 in (0,1,1) and P2 in (0,2,1) and P1 in ((0,0,2) or (0,0,3) or (0,1,3))
    #random((0,2,3),(0,3,2),(0,3,3))

#if P1 in (0,1,1) and P2 in (0,2,2) and P1 in ((0,2,0) or (0,3,0) or (0,3,1))
    #random((0,0,2),(0,0,3),(0,1,3))

#if P1 in (0,1,1) and P2 in (0,2,2) and P1 in ((0,0,2) or (0,0,3) or (0,1,3))
    #random((0,2,0),(0,3,0),(0,3,1))


#Player 1 case 2
#if P1 in (0,2,1) and P2 in (0,1,1)
    #random((0,2,3),(0,3,2),(0,3,3))

#if P1 in (0,2,1) and P2 in (0,2,2)
    #random((0,0,0),(0,0,1),(0,1,0))

#if P1 in (0,2,1) and P2 in (0,1,2)
    #random((0,2,3),(0,3,2),(0,3,3),(0,0,0),(0,0,1),(0,1,0))

#Player 2 case 2
#if P1 in (0,2,1) and P2 in (0,1,1) and P1 in ((0,2,3) or (0,3,2) or (0,3,3))
    #random((0,0,2),(0,0,3),(0,1,3))

#if P1 in (0,2,1) and P2 in (0,2,2) and P1 in ((0,0,0) or (0,0,1) or (0,1,0))
    #random((0,0,2),(0,0,3),(0,1,3))

#if P1 in (0,2,1) and P2 in (0,1,2) and P1 in ((0,2,3) or (0,3,2) or (0,3,3))
    #random((0,0,0),(0,0,1),(0,1,0))

#if P1 in (0,2,1) and P2 in (0,1,2) and P1 in ((0,0,0) or (0,0,1) or (0,1,0))
    #random((0,2,3),(0,3,2),(0,3,3))


#Player 1 case 3
#if P1 in (0,1,2) and P2 in (0,1,1)
    #random((0,2,3),(0,3,2),(0,3,3))

#if P1 in (0,1,2) and P2 in (0,2,2)
    #random((0,0,0),(0,0,1),(0,1,0))

#if P1 in (0,1,2) and P2 in (0,2,1)
    #random((0,2,3),(0,3,2),(0,3,3),(0,0,0),(0,0,1),(0,1,0))

#Player 2 case 3
#if P1 in (0,1,2) and P2 in (0,1,1) and P1 in ((0,2,3) or (0,3,2) or (0,3,3))
    #random((0,2,0),(0,3,0),(0,3,1))

#if P1 in (0,1,2) and P2 in (0,2,2) and P1 in ((0,0,0) or (0,0,1) or (0,1,0))
    #random((0,2,0),(0,3,0),(0,3,1))

#if P1 in (0,1,2) and P2 in (0,2,1) and P1 in ((0,2,3) or (0,3,2) or (0,3,3))
    #random((0,0,0),(0,0,1),(0,1,0))

#if P1 in (0,1,2) and P2 in (0,2,1) and P1 in ((0,0,0) or (0,0,1) or (0,1,0))
    #random((0,2,3),(0,3,2),(0,3,3))


#Player 1 case 4
#if P1 in (0,2,2) and P2 in (0,2,1)
    #random((0,0,2),(0,0,3),(0,1,3))

#if P1 in (0,2,2) and P2 in (0,1,2)
    #random((0,2,0),(0,3,0),(0,3,1))

#if P1 in (0,2,2) and P2 in (0,1,1)
    #random((0,0,2),(0,0,3),(0,1,3),(0,2,0),(0,3,0),(0,3,1))

#Player 2 case 4
#if P1 in (0,2,2) and P2 in (0,2,1) and P1 in ((0,0,2) or (0,0,3) or (0,1,3))
    #random((0,0,0),(0,0,1),(0,1,0))

#if P1 in (0,2,2) and P2 in (0,1,2) and P1 in ((0,2,0) or (0,3,0) or (0,3,1))
    #random((0,0,0),(0,0,1),(0,1,0))

#if P1 in (0,2,2) and P2 in (0,1,1) and P1 in ((0,0,2) or (0,0,3) or (0,1,3))
    #random((0,2,0),(0,3,0),(0,3,1))

#if P1 in (0,2,2) and P2 in (0,1,1) and P1 in ((0,2,0) or (0,3,0) or (0,3,1))
    #random((0,0,2),(0,0,3),(0,1,3))
