class Expr:
    def accept(self, visitor):
        raise NotImplementedError


class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitBinaryExpr(self)


class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitGroupingExpr(self)


class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visitLiteralExpr(self)


class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitUnaryExpr(self)


class Variable(Expr):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visitVariableExpr(self)


class Assign(Expr):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visitAssignExpr(self)


class Logical(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitLogicalExpr(self)


class Call(Expr):
    def __init__(self, callee, paren, arguments):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visitCallExpr(self)


class Get(Expr):
    def __init__(self, obj, name):
        self.object = obj
        self.name = name

    def accept(self, visitor):
        return visitor.visitGetExpr(self)


class Set(Expr):
    def __init__(self, obj, name, value):
        self.object = obj
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visitSetExpr(self)


class This(Expr):
    def __init__(self, keyword):
        self.keyword = keyword

    def accept(self, visitor):
        return visitor.visitThisExpr(self)


class Super(Expr):
    def __init__(self, keyword, method):
        self.keyword = keyword
        self.method = method

    def accept(self, visitor):
        return visitor.visitSuperExpr(self)
