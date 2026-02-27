;; simpsons.clp
;; Family relationship inference rules

;; CHILD
;; If Y is parent of X, then X is child of Y
(defrule child-rule
(parentOf ?child ?parent)
=>
(assert (childOf ?child ?parent))
)


;; MOTHER
(defrule mother-rule
(parentOf ?child ?parent)
(female ?parent)
=>
(assert (motherOf ?parent ?child))
)


;; FATHER
(defrule father-rule
(parentOf ?child ?parent)
(male ?parent)
=>
(assert (fatherOf ?parent ?child))
)


;; SIBLINGS
;; Share at least one parent
(defrule sibling-rule
(parentOf ?x ?p)
(parentOf ?y ?p)
(test (neq ?x ?y))
=>
(assert (sibling ?x ?y))
)


;; BROTHER
(defrule brother-rule
(sibling ?x ?y)
(male ?x)
=>
(assert (brother ?x ?y))
)


;; SISTER
(defrule sister-rule
(sibling ?x ?y)
(female ?x)
=>
(assert (sister ?x ?y))
)


;; GRANDPARENT
(defrule grandparent-rule
(parentOf ?child ?parent)
(parentOf ?parent ?grandparent)
=>
(assert (grandparent ?grandparent ?child))
)


;; GRANDMOTHER
(defrule grandmother-rule
(grandparent ?g ?c)
(female ?g)
=>
(assert (grandmother ?g ?c))
)


;; GRANDFATHER
(defrule grandfather-rule
(grandparent ?g ?c)
(male ?g)
=>
(assert (grandfather ?g ?c))
)
