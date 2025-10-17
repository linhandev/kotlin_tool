# Generated from KotlinParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .KotlinParser import KotlinParser
else:
    from KotlinParser import KotlinParser

# This class defines a complete generic visitor for a parse tree produced by KotlinParser.

class KotlinParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by KotlinParser#kotlinFile.
    def visitKotlinFile(self, ctx:KotlinParser.KotlinFileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#script.
    def visitScript(self, ctx:KotlinParser.ScriptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#fileAnnotation.
    def visitFileAnnotation(self, ctx:KotlinParser.FileAnnotationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#packageHeader.
    def visitPackageHeader(self, ctx:KotlinParser.PackageHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#importList.
    def visitImportList(self, ctx:KotlinParser.ImportListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#importHeader.
    def visitImportHeader(self, ctx:KotlinParser.ImportHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#importAlias.
    def visitImportAlias(self, ctx:KotlinParser.ImportAliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#topLevelObject.
    def visitTopLevelObject(self, ctx:KotlinParser.TopLevelObjectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#classDeclaration.
    def visitClassDeclaration(self, ctx:KotlinParser.ClassDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#primaryConstructor.
    def visitPrimaryConstructor(self, ctx:KotlinParser.PrimaryConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#classParameters.
    def visitClassParameters(self, ctx:KotlinParser.ClassParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#classParameter.
    def visitClassParameter(self, ctx:KotlinParser.ClassParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#delegationSpecifiers.
    def visitDelegationSpecifiers(self, ctx:KotlinParser.DelegationSpecifiersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#annotatedDelegationSpecifier.
    def visitAnnotatedDelegationSpecifier(self, ctx:KotlinParser.AnnotatedDelegationSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#delegationSpecifier.
    def visitDelegationSpecifier(self, ctx:KotlinParser.DelegationSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#constructorInvocation.
    def visitConstructorInvocation(self, ctx:KotlinParser.ConstructorInvocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#explicitDelegation.
    def visitExplicitDelegation(self, ctx:KotlinParser.ExplicitDelegationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#classBody.
    def visitClassBody(self, ctx:KotlinParser.ClassBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#classMemberDeclarations.
    def visitClassMemberDeclarations(self, ctx:KotlinParser.ClassMemberDeclarationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#classMemberDeclaration.
    def visitClassMemberDeclaration(self, ctx:KotlinParser.ClassMemberDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#anonymousInitializer.
    def visitAnonymousInitializer(self, ctx:KotlinParser.AnonymousInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#secondaryConstructor.
    def visitSecondaryConstructor(self, ctx:KotlinParser.SecondaryConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#constructorDelegationCall.
    def visitConstructorDelegationCall(self, ctx:KotlinParser.ConstructorDelegationCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#enumClassBody.
    def visitEnumClassBody(self, ctx:KotlinParser.EnumClassBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#enumEntries.
    def visitEnumEntries(self, ctx:KotlinParser.EnumEntriesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#enumEntry.
    def visitEnumEntry(self, ctx:KotlinParser.EnumEntryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#functionDeclaration.
    def visitFunctionDeclaration(self, ctx:KotlinParser.FunctionDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#functionValueParameters.
    def visitFunctionValueParameters(self, ctx:KotlinParser.FunctionValueParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#functionValueParameter.
    def visitFunctionValueParameter(self, ctx:KotlinParser.FunctionValueParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#parameter.
    def visitParameter(self, ctx:KotlinParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#setterParameter.
    def visitSetterParameter(self, ctx:KotlinParser.SetterParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#functionBody.
    def visitFunctionBody(self, ctx:KotlinParser.FunctionBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#objectDeclaration.
    def visitObjectDeclaration(self, ctx:KotlinParser.ObjectDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#companionObject.
    def visitCompanionObject(self, ctx:KotlinParser.CompanionObjectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#propertyDeclaration.
    def visitPropertyDeclaration(self, ctx:KotlinParser.PropertyDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#multiVariableDeclaration.
    def visitMultiVariableDeclaration(self, ctx:KotlinParser.MultiVariableDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#variableDeclaration.
    def visitVariableDeclaration(self, ctx:KotlinParser.VariableDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#propertyDelegate.
    def visitPropertyDelegate(self, ctx:KotlinParser.PropertyDelegateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#getter.
    def visitGetter(self, ctx:KotlinParser.GetterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#setter.
    def visitSetter(self, ctx:KotlinParser.SetterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#typeAlias.
    def visitTypeAlias(self, ctx:KotlinParser.TypeAliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#typeParameters.
    def visitTypeParameters(self, ctx:KotlinParser.TypeParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#typeParameter.
    def visitTypeParameter(self, ctx:KotlinParser.TypeParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#typeParameterModifiers.
    def visitTypeParameterModifiers(self, ctx:KotlinParser.TypeParameterModifiersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#typeParameterModifier.
    def visitTypeParameterModifier(self, ctx:KotlinParser.TypeParameterModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#type_.
    def visitType_(self, ctx:KotlinParser.Type_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#typeModifiers.
    def visitTypeModifiers(self, ctx:KotlinParser.TypeModifiersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#typeModifier.
    def visitTypeModifier(self, ctx:KotlinParser.TypeModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#parenthesizedType.
    def visitParenthesizedType(self, ctx:KotlinParser.ParenthesizedTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#nullableType.
    def visitNullableType(self, ctx:KotlinParser.NullableTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#typeReference.
    def visitTypeReference(self, ctx:KotlinParser.TypeReferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#functionType.
    def visitFunctionType(self, ctx:KotlinParser.FunctionTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#receiverType.
    def visitReceiverType(self, ctx:KotlinParser.ReceiverTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#userType.
    def visitUserType(self, ctx:KotlinParser.UserTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#parenthesizedUserType.
    def visitParenthesizedUserType(self, ctx:KotlinParser.ParenthesizedUserTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#simpleUserType.
    def visitSimpleUserType(self, ctx:KotlinParser.SimpleUserTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#functionTypeParameters.
    def visitFunctionTypeParameters(self, ctx:KotlinParser.FunctionTypeParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#typeConstraints.
    def visitTypeConstraints(self, ctx:KotlinParser.TypeConstraintsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#typeConstraint.
    def visitTypeConstraint(self, ctx:KotlinParser.TypeConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#block.
    def visitBlock(self, ctx:KotlinParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#statements.
    def visitStatements(self, ctx:KotlinParser.StatementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#statement.
    def visitStatement(self, ctx:KotlinParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#declaration.
    def visitDeclaration(self, ctx:KotlinParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#assignment.
    def visitAssignment(self, ctx:KotlinParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#expression.
    def visitExpression(self, ctx:KotlinParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#disjunction.
    def visitDisjunction(self, ctx:KotlinParser.DisjunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#conjunction.
    def visitConjunction(self, ctx:KotlinParser.ConjunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#equality.
    def visitEquality(self, ctx:KotlinParser.EqualityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#comparison.
    def visitComparison(self, ctx:KotlinParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#infixOperation.
    def visitInfixOperation(self, ctx:KotlinParser.InfixOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#elvisExpression.
    def visitElvisExpression(self, ctx:KotlinParser.ElvisExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#infixFunctionCall.
    def visitInfixFunctionCall(self, ctx:KotlinParser.InfixFunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#rangeExpression.
    def visitRangeExpression(self, ctx:KotlinParser.RangeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#additiveExpression.
    def visitAdditiveExpression(self, ctx:KotlinParser.AdditiveExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#multiplicativeExpression.
    def visitMultiplicativeExpression(self, ctx:KotlinParser.MultiplicativeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#asExpression.
    def visitAsExpression(self, ctx:KotlinParser.AsExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#prefixUnaryExpression.
    def visitPrefixUnaryExpression(self, ctx:KotlinParser.PrefixUnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#unaryPrefix.
    def visitUnaryPrefix(self, ctx:KotlinParser.UnaryPrefixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#postfixUnaryExpression.
    def visitPostfixUnaryExpression(self, ctx:KotlinParser.PostfixUnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#postfixUnarySuffix.
    def visitPostfixUnarySuffix(self, ctx:KotlinParser.PostfixUnarySuffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#directlyAssignableExpression.
    def visitDirectlyAssignableExpression(self, ctx:KotlinParser.DirectlyAssignableExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#assignableExpression.
    def visitAssignableExpression(self, ctx:KotlinParser.AssignableExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#assignableSuffix.
    def visitAssignableSuffix(self, ctx:KotlinParser.AssignableSuffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#indexingSuffix.
    def visitIndexingSuffix(self, ctx:KotlinParser.IndexingSuffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#navigationSuffix.
    def visitNavigationSuffix(self, ctx:KotlinParser.NavigationSuffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#callSuffix.
    def visitCallSuffix(self, ctx:KotlinParser.CallSuffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#annotatedLambda.
    def visitAnnotatedLambda(self, ctx:KotlinParser.AnnotatedLambdaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#valueArguments.
    def visitValueArguments(self, ctx:KotlinParser.ValueArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#typeArguments.
    def visitTypeArguments(self, ctx:KotlinParser.TypeArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#typeProjection.
    def visitTypeProjection(self, ctx:KotlinParser.TypeProjectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#typeProjectionModifiers.
    def visitTypeProjectionModifiers(self, ctx:KotlinParser.TypeProjectionModifiersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#typeProjectionModifier.
    def visitTypeProjectionModifier(self, ctx:KotlinParser.TypeProjectionModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#valueArgument.
    def visitValueArgument(self, ctx:KotlinParser.ValueArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#primaryExpression.
    def visitPrimaryExpression(self, ctx:KotlinParser.PrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#parenthesizedExpression.
    def visitParenthesizedExpression(self, ctx:KotlinParser.ParenthesizedExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#collectionLiteral.
    def visitCollectionLiteral(self, ctx:KotlinParser.CollectionLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#literalConstant.
    def visitLiteralConstant(self, ctx:KotlinParser.LiteralConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#stringLiteral.
    def visitStringLiteral(self, ctx:KotlinParser.StringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#lineStringLiteral.
    def visitLineStringLiteral(self, ctx:KotlinParser.LineStringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#multiLineStringLiteral.
    def visitMultiLineStringLiteral(self, ctx:KotlinParser.MultiLineStringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#lineStringContent.
    def visitLineStringContent(self, ctx:KotlinParser.LineStringContentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#lineStringExpression.
    def visitLineStringExpression(self, ctx:KotlinParser.LineStringExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#multiLineStringContent.
    def visitMultiLineStringContent(self, ctx:KotlinParser.MultiLineStringContentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#multiLineStringExpression.
    def visitMultiLineStringExpression(self, ctx:KotlinParser.MultiLineStringExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#lambdaLiteral.
    def visitLambdaLiteral(self, ctx:KotlinParser.LambdaLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#lambdaParameters.
    def visitLambdaParameters(self, ctx:KotlinParser.LambdaParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#lambdaParameter.
    def visitLambdaParameter(self, ctx:KotlinParser.LambdaParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#anonymousFunction.
    def visitAnonymousFunction(self, ctx:KotlinParser.AnonymousFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#functionLiteral.
    def visitFunctionLiteral(self, ctx:KotlinParser.FunctionLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#objectLiteral.
    def visitObjectLiteral(self, ctx:KotlinParser.ObjectLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#thisExpression.
    def visitThisExpression(self, ctx:KotlinParser.ThisExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#superExpression.
    def visitSuperExpression(self, ctx:KotlinParser.SuperExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#controlStructureBody.
    def visitControlStructureBody(self, ctx:KotlinParser.ControlStructureBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#ifExpression.
    def visitIfExpression(self, ctx:KotlinParser.IfExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#whenExpression.
    def visitWhenExpression(self, ctx:KotlinParser.WhenExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#whenEntry.
    def visitWhenEntry(self, ctx:KotlinParser.WhenEntryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#whenCondition.
    def visitWhenCondition(self, ctx:KotlinParser.WhenConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#rangeTest.
    def visitRangeTest(self, ctx:KotlinParser.RangeTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#typeTest.
    def visitTypeTest(self, ctx:KotlinParser.TypeTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#tryExpression.
    def visitTryExpression(self, ctx:KotlinParser.TryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#catchBlock.
    def visitCatchBlock(self, ctx:KotlinParser.CatchBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#finallyBlock.
    def visitFinallyBlock(self, ctx:KotlinParser.FinallyBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#loopStatement.
    def visitLoopStatement(self, ctx:KotlinParser.LoopStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#forStatement.
    def visitForStatement(self, ctx:KotlinParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#whileStatement.
    def visitWhileStatement(self, ctx:KotlinParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#doWhileStatement.
    def visitDoWhileStatement(self, ctx:KotlinParser.DoWhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#jumpExpression.
    def visitJumpExpression(self, ctx:KotlinParser.JumpExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#callableReference.
    def visitCallableReference(self, ctx:KotlinParser.CallableReferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#assignmentAndOperator.
    def visitAssignmentAndOperator(self, ctx:KotlinParser.AssignmentAndOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#equalityOperator.
    def visitEqualityOperator(self, ctx:KotlinParser.EqualityOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#comparisonOperator.
    def visitComparisonOperator(self, ctx:KotlinParser.ComparisonOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#inOperator.
    def visitInOperator(self, ctx:KotlinParser.InOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#isOperator.
    def visitIsOperator(self, ctx:KotlinParser.IsOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#additiveOperator.
    def visitAdditiveOperator(self, ctx:KotlinParser.AdditiveOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#multiplicativeOperator.
    def visitMultiplicativeOperator(self, ctx:KotlinParser.MultiplicativeOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#asOperator.
    def visitAsOperator(self, ctx:KotlinParser.AsOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#prefixUnaryOperator.
    def visitPrefixUnaryOperator(self, ctx:KotlinParser.PrefixUnaryOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#postfixUnaryOperator.
    def visitPostfixUnaryOperator(self, ctx:KotlinParser.PostfixUnaryOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#memberAccessOperator.
    def visitMemberAccessOperator(self, ctx:KotlinParser.MemberAccessOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#modifiers.
    def visitModifiers(self, ctx:KotlinParser.ModifiersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#modifier.
    def visitModifier(self, ctx:KotlinParser.ModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#classModifier.
    def visitClassModifier(self, ctx:KotlinParser.ClassModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#memberModifier.
    def visitMemberModifier(self, ctx:KotlinParser.MemberModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#visibilityModifier.
    def visitVisibilityModifier(self, ctx:KotlinParser.VisibilityModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#varianceModifier.
    def visitVarianceModifier(self, ctx:KotlinParser.VarianceModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#functionModifier.
    def visitFunctionModifier(self, ctx:KotlinParser.FunctionModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#propertyModifier.
    def visitPropertyModifier(self, ctx:KotlinParser.PropertyModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#inheritanceModifier.
    def visitInheritanceModifier(self, ctx:KotlinParser.InheritanceModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#parameterModifier.
    def visitParameterModifier(self, ctx:KotlinParser.ParameterModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#reificationModifier.
    def visitReificationModifier(self, ctx:KotlinParser.ReificationModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#platformModifier.
    def visitPlatformModifier(self, ctx:KotlinParser.PlatformModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#label.
    def visitLabel(self, ctx:KotlinParser.LabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#annotation.
    def visitAnnotation(self, ctx:KotlinParser.AnnotationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#singleAnnotation.
    def visitSingleAnnotation(self, ctx:KotlinParser.SingleAnnotationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#multiAnnotation.
    def visitMultiAnnotation(self, ctx:KotlinParser.MultiAnnotationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#annotationUseSiteTarget.
    def visitAnnotationUseSiteTarget(self, ctx:KotlinParser.AnnotationUseSiteTargetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#unescapedAnnotation.
    def visitUnescapedAnnotation(self, ctx:KotlinParser.UnescapedAnnotationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#simpleIdentifier.
    def visitSimpleIdentifier(self, ctx:KotlinParser.SimpleIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#identifier.
    def visitIdentifier(self, ctx:KotlinParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#shebangLine.
    def visitShebangLine(self, ctx:KotlinParser.ShebangLineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#quest.
    def visitQuest(self, ctx:KotlinParser.QuestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#elvis.
    def visitElvis(self, ctx:KotlinParser.ElvisContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#safeNav.
    def visitSafeNav(self, ctx:KotlinParser.SafeNavContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#excl.
    def visitExcl(self, ctx:KotlinParser.ExclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#semi.
    def visitSemi(self, ctx:KotlinParser.SemiContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KotlinParser#semis.
    def visitSemis(self, ctx:KotlinParser.SemisContext):
        return self.visitChildren(ctx)



del KotlinParser