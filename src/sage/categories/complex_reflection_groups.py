r"""
Complex reflection groups
"""
#*****************************************************************************
#       Copyright (C) 2011-2015 Christian Stump <christian.stump at gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.misc.abstract_method import abstract_method
from sage.misc.all import prod
from sage.misc.cachefunc import cached_method
from sage.misc.lazy_import import LazyImport
from sage.categories.category_singleton import Category_singleton
from sage.categories.category_with_axiom import CategoryWithAxiom, axiom
from sage.categories.groups import Groups

class ComplexReflectionGroups(Category_singleton):
    r"""
    The category of finite dimensional complex reflection groups.

    This is the base category for subgroups of the special linear
    group which are generated by reflections.

    A *reflection group* is a group `W` generated by (complex)
    reflections `t \in \operatorname{O}(V)` acting on a complex vector
    space `V` such that `t` fixes a hyperplane pointwise and acts by a
    root of unity on its orthogonal complement.

    The (finite) dimension of `V` is the *rank* of `W`.

    For a comprehensive treatment of complex reflection groups and
    many definitions and theorems used here, we refer to [LT2009]_.
    See also :wikipedia:`Reflection_group`.

    .. SEEALSO::

        :func:`ReflectionGroup` for usage examples of this category.

    REFERENCES:

    .. [LT2009] G. I. Lehrer and D. E. Taylor. Unitary reflection groups. Australian Mathematical Society Lecture Series, 2009.

    EXAMPLES::

        sage: ComplexReflectionGroups()
        Category of complex reflection groups
        sage: ComplexReflectionGroups().super_categories()
        [Category of groups]
        sage: ComplexReflectionGroups().all_super_categories()
        [Category of complex reflection groups,
         Category of groups,
         Category of monoids,
         Category of semigroups,
         Category of inverse unital magmas,
         Category of unital magmas,
         Category of magmas,
         Category of sets,
         Category of sets with partial maps,
         Category of objects]

    An example of a reflection group::

        sage: W = ComplexReflectionGroups().example(); W
        5-colored permutations of size 3

    ``W`` is in the category of complex reflection groups::

        sage: W in ComplexReflectionGroups()
        True

    TESTS::

        sage: TestSuite(W).run()
        sage: TestSuite(ComplexReflectionGroups()).run()
    """

    @cached_method
    def super_categories(self):
        r"""
        Return the super categories of ``self``.

        EXAMPLES::

            sage: ComplexReflectionGroups().super_categories()
            [Category of groups]
        """
        return [Groups()]

    class SubcategoryMethods:
        Finite = axiom("Finite")
        Irreducible = axiom("Irreducible")
        WellGenerated = axiom("WellGenerated")

    def example(self):
        r"""
        Return an example of a complex reflection group.

        EXAMPLES::

            sage: ComplexReflectionGroups().example()
            5-colored permutations of size 3
        """
        from sage.combinat.colored_permutations import ColoredPermutations
        return ColoredPermutations(5, 3)

    class ParentMethods:

        @abstract_method
        def index_set(self):
            r"""
            Return the index set of the simple reflections of ``self``.

            EXAMPLES::

                sage: W = ColoredPermutations(1,4)
                sage: W.index_set()
                (1, 2, 3)
                sage: W = ReflectionGroup((1,1,4),index_set=[1,3,'asdf'])
                sage: W.index_set()
                [1, 3, 'asdf']
                sage: W = ReflectionGroup((1,1,4),index_set={'a':0,'b':1,'c':2})
                sage: W.index_set()
                ['a', 'b', 'c']
            """

        def simple_reflection(self, i):
            r"""
            Return the `i`-th simple reflection of ``self``.

            For `i` in `1,\dots,n`, this gives the `i`-th simple reflection of ``self``.

            EXAMPLES::

                sage: W = ReflectionGroup((1,1,4),index_set=[1,3,'asdf'])
                sage: for i in W.index_set():
                ....:     print i, W.simple_reflection(i)
                1 (1,7)(2,4)(5,6)(8,10)(11,12)
                3 (1,4)(2,8)(3,5)(7,10)(9,11)
                asdf (2,5)(3,9)(4,6)(8,11)(10,12)
            """
            return self.one().apply_simple_reflection(i)

        @abstract_method(optional=True)
        def hyperplane_index_set(self):
            r"""
            Return the index set of the reflection hyperplanes of
            ``self``.

            EXAMPLES::

                sage: W = ColoredPermutations(1,4)
                sage: W.hyperplane_index_set()
                [0, 1, 2, 3, 4, 5]
                sage: W = ReflectionGroup((1,1,4),hyperplane_index_set=[1,3,'asdf',7,9,11])
                sage: W.hyperplane_index_set()
                [1, 3, 'asdf', 7, 9, 11]
                sage: W = ReflectionGroup((1,1,4),hyperplane_index_set={'a':0,'b':1,'c':2,'d':3,'e':4,'f':5})
                sage: W.hyperplane_index_set()
                ['a', 'b', 'c', 'd', 'e', 'f']
            """

        @abstract_method(optional=True)
        def distinguished_reflection(self, i):
            r"""
            Return the `i`-th distinguished reflection of ``self``.

            For `i` in `1,\dots,N^*`, this gives the `i`-th distinguished reflection of ``self``.
            For a definition of destinguished reflections, see :meth:`distinguished_reflections`.

            EXAMPLES::

                sage: W = ReflectionGroup((1,1,4),hyperplane_index_set={'a':0,'b':1,'c':2,'d':3,'e':4,'f':5})
                sage: for i in W.hyperplane_index_set(): print i, W.distinguished_reflection(i)
                a (1,7)(2,4)(5,6)(8,10)(11,12)
                b (1,4)(2,8)(3,5)(7,10)(9,11)
                c (2,5)(3,9)(4,6)(8,11)(10,12)
                d (1,8)(2,7)(3,6)(4,10)(9,12)
                e (1,6)(2,9)(3,8)(5,11)(7,12)
                f (1,11)(3,10)(4,9)(5,7)(6,12)
            """

        @abstract_method(optional=True)
        def reflection_index_set(self):
            r"""
            Return the index set of the reflections of ``self``.

            EXAMPLES::

                sage: W = ColoredPermutations(1,4)
                sage: W.reflection_index_set()
                [0, 1, 2, 3, 4, 5]
                sage: W = ReflectionGroup((1,1,4),reflection_index_set=[1,3,'asdf',7,9,11])
                sage: W.reflection_index_set()
                [1, 3, 'asdf', 7, 9, 11]
                sage: W = ReflectionGroup((1,1,4),reflection_index_set={'a':0,'b':1,'c':2,'d':3,'e':4,'f':5})
                sage: W.reflection_index_set()
                ['a', 'b', 'c', 'd', 'e', 'f']
            """

        @abstract_method(optional=True)
        def reflection(self, i):
            r"""
            Return the `i`-th reflection of ``self``.

            For `i` in `1,\dots,N`, this gives the `i`-th reflection of
            ``self``.

            EXAMPLES::

                sage: W = ColoredPermutations(1,4)
                sage: for i in W.reflection_index_set():
                ....:     print i, W.reflection(i)
                0 (1,7)(2,4)(5,6)(8,10)(11,12)
                1 (1,4)(2,8)(3,5)(7,10)(9,11)
                2 (2,5)(3,9)(4,6)(8,11)(10,12)
                3 (1,8)(2,7)(3,6)(4,10)(9,12)
                4 (1,6)(2,9)(3,8)(5,11)(7,12)
                5 (1,11)(3,10)(4,9)(5,7)(6,12)
            """

        @cached_method
        def simple_reflections(self):
            r"""
            Return the simple reflections of ``self`` as a family
            indexed by :meth:`index_set`.

            EXAMPLES::

                sage: W = ColoredPermutations(1,3)
                sage: W.simple_reflections()
                Finite family {1: [[0, 0, 0], [2, 1, 3]], 2: [[0, 0, 0], [1, 3, 2]]}

                sage: W = ReflectionGroup((1,1,3),index_set=['a','b'])
                sage: W.simple_reflections()
                Finite family {'a': (1,4)(2,3)(5,6), 'b': (1,3)(2,5)(4,6)}
            """
            from sage.sets.family import Family
            return Family(self.index_set(), self.simple_reflection)

        @cached_method
        def distinguished_reflections(self):
            r"""
            Return a finite family containing the distinguished
            reflections of ``self``, indexed by
            :meth:`hyperplane_index_set`.

            These are the reflections in ``self`` acting on the
            complement of the fixed hyperplane `H` as
            `\operatorname{exp}(2 \pi i / n)`, where `n` is the order of
            the reflection subgroup fixing `H`.

           EXAMPLES::

                sage: W = ColoredPermutations(1,3)
                sage: distinguished_reflections = W.distinguished_reflections()
                sage: for index in sorted(distinguished_reflections.keys()): print index, distinguished_reflections[index]
                0 (1,4)(2,3)(5,6)
                1 (1,3)(2,5)(4,6)
                2 (1,5)(2,4)(3,6)

                sage: W = ReflectionGroup((1,1,3),hyperplane_index_set=['a','b','c'])
                sage: distinguished_reflections = W.distinguished_reflections()
                sage: for index in sorted(distinguished_reflections.keys()): print index, distinguished_reflections[index]
                a (1,4)(2,3)(5,6)
                b (1,3)(2,5)(4,6)
                c (1,5)(2,4)(3,6)

                sage: W = ColoredPermutations(3,1)
                sage: distinguished_reflections = W.distinguished_reflections()
                sage: for index in sorted(distinguished_reflections.keys()): print index, distinguished_reflections[index]
                0 (1,2,3)

                sage: W = ReflectionGroup((1,1,3),(3,1,2))
                sage: distinguished_reflections = W.distinguished_reflections()
                sage: for index in sorted(distinguished_reflections.keys()): print index, distinguished_reflections[index]
                0 (1,6)(2,5)(7,8)
                1 (1,5)(2,7)(6,8)
                2 (3,9,15)(4,10,16)(12,17,23)(14,18,24)(20,25,29)(21,22,26)(27,28,30)
                3 (3,11)(4,12)(9,13)(10,14)(15,19)(16,20)(17,21)(18,22)(23,27)(24,28)(25,26)(29,30)
                4 (1,7)(2,6)(5,8)
                5 (3,19)(4,25)(9,11)(10,17)(12,28)(13,15)(14,30)(16,18)(20,27)(21,29)(22,23)(24,26)
                6 (4,21,27)(10,22,28)(11,13,19)(12,14,20)(16,26,30)(17,18,25)(23,24,29)
                7 (3,13)(4,24)(9,19)(10,29)(11,15)(12,26)(14,21)(16,23)(17,30)(18,27)(20,22)(25,28)
            """
            from sage.sets.family import Family
            return Family(self.hyperplane_index_set(), self.distinguished_reflection)

        @cached_method
        def reflections(self):
            r"""
            Return a finite family containing the reflections of
            ``self``, indexed by :meth:`reflection_index_set`.

           EXAMPLES::

                sage: W = ColoredPermutations(1,3)
                sage: reflections = W.reflections()
                sage: for index in sorted(reflections.keys()): print index, reflections[index]
                0 (1,4)(2,3)(5,6)
                1 (1,3)(2,5)(4,6)
                2 (1,5)(2,4)(3,6)

                sage: W = ReflectionGroup((1,1,3),reflection_index_set=['a','b','c'])
                sage: reflections = W.reflections()
                sage: for index in sorted(reflections.keys()): print index, reflections[index]
                a (1,4)(2,3)(5,6)
                b (1,3)(2,5)(4,6)
                c (1,5)(2,4)(3,6)

                sage: W = ColoredPermutations(3,1)
                sage: reflections = W.reflections()
                sage: for index in sorted(reflections.keys()): print index, reflections[index]
                0 (1,2,3)
                1 (1,3,2)

                sage: W = ReflectionGroup((1,1,3),(3,1,2))
                sage: reflections = W.reflections()
                sage: for index in sorted(reflections.keys()): print index, reflections[index]
                0 (1,6)(2,5)(7,8)
                1 (1,5)(2,7)(6,8)
                2 (3,9,15)(4,10,16)(12,17,23)(14,18,24)(20,25,29)(21,22,26)(27,28,30)
                3 (3,11)(4,12)(9,13)(10,14)(15,19)(16,20)(17,21)(18,22)(23,27)(24,28)(25,26)(29,30)
                4 (1,7)(2,6)(5,8)
                5 (3,19)(4,25)(9,11)(10,17)(12,28)(13,15)(14,30)(16,18)(20,27)(21,29)(22,23)(24,26)
                6 (4,21,27)(10,22,28)(11,13,19)(12,14,20)(16,26,30)(17,18,25)(23,24,29)
                7 (3,13)(4,24)(9,19)(10,29)(11,15)(12,26)(14,21)(16,23)(17,30)(18,27)(20,22)(25,28)
                8 (3,15,9)(4,16,10)(12,23,17)(14,24,18)(20,29,25)(21,26,22)(27,30,28)
                9 (4,27,21)(10,28,22)(11,19,13)(12,20,14)(16,30,26)(17,25,18)(23,29,24)
            """
            from sage.sets.family import Family
            return Family(self.reflection_index_set(), self.reflection)

        def nr_simple_reflections(self):
            r"""
            Return the number of simple reflections of ``self``.

            EXAMPLES::

                sage: W = ColoredPermutations(1,3)
                sage: W.nr_simple_reflections()
                2
                sage: W = ColoredPermutations(2,3)
                sage: W.nr_simple_reflections()
                3
                sage: W = ColoredPermutations(4,3)
                sage: W.nr_simple_reflections()
                3
                sage: W = ReflectionGroup((4,2,3))
                sage: W.nr_simple_reflections()
                4
            """
            return len(self.simple_reflections())

        @abstract_method(optional=True)
        def irreducible_components(self):
            r"""
            Return a list containing all irreducible components of
            ``self`` as finite reflection groups.

            EXAMPLES::

                sage: W = ReflectionGroup([1,1,3],[3,1,3],4)
                sage: W.irreducible_components()
                [Irreducible real reflection group of rank 2 and type A2,
                 Irreducible complex reflection group of rank 3 and type G(3,1,3),
                 Irreducible complex reflection group of rank 2 and type ST4]
            """

        def an_element(self):
            r"""
            Return the product of the simple reflections of ``self``.

            EXAMPLES::

                sage: W = ComplexReflectionGroups().example()
                sage: W
                5-colored permutations of size 3
                sage: W.an_element()
                [[1, 0, 0], [3, 1, 2]]
            """
            return self.prod(self.reflection(i) for i in self.index_set())

        def some_elements(self):
            r"""
            Return a list of typical elements of ``self``.

            Implements :meth:`Sets.ParentMethods.some_elements` by
            returning some typical element of ``self``.

            EXAMPLES::

                sage: W = ColoredPermutations(1,4)
                sage: W.some_elements()
                [[[0, 0, 0, 0], [2, 1, 3, 4]],
                 [[0, 0, 0, 0], [1, 3, 2, 4]],
                 [[0, 0, 0, 0], [1, 2, 4, 3]],
                 [[0, 0, 0, 0], [1, 2, 3, 4]],
                 [[0, 0, 0, 0], [4, 1, 2, 3]]]
                sage: W.order()
                24
            """
            prod_ref = self.prod(self.reflection(i) for i in self.index_set())
            return list(self.simple_reflections()) + [self.one(), self.an_element(), prod_ref]

        def from_word(self, word, word_type='simple'):
            r"""
            Return the reflection group element corresponding to
            ``word``.

            INPUT:

            - ``word`` -- a list (or iterable) of elements of the
              appropriate index set

            - ``word_type`` -- (optional, default: ``'simple'``) can be
              ``'simple'``, ``'distinguished'``, or ``'all'``, depending
              on the type of reflections used

            If ``word`` is `[i_1, i_2, \ldots, i_k]`, then this returns the
            corresponding product of (simple/distinguished/all)
            reflections `t_{i_1} t_{i_2} \cdots t_{i_k}`.

            EXAMPLES::

                sage: W = ColoredPermutations(1,4); W
                1-colored permutations of size 4
                sage: W.from_word([1,2,1,2,1,2])
                [[0, 0, 0, 0], [1, 2, 3, 4]]

                sage: W.from_word([1, 2, 3]).reduced_word()
                [1, 2, 3]

                sage: W.from_word([0,1,2], word_type='all').reduced_word()
                word: 012

                sage: W.from_word([0,1,2], word_type='all').reduced_word_in_reflections()
                word: 012

                sage: W.from_word([0,1,2]).reduced_word_in_reflections()
                word: 012
            """
            if word_type == 'simple':
                f = self.one().apply_simple_reflections
            elif word_type == 'distinguished':
                f = self.one().apply_distinguished_reflections
            elif word_type == 'all':
                f = self.one().apply_reflections
            return f(word, side='right')

        def group_generators(self):
            r"""
            Return the simple reflections of ``self``.

            Implements :meth:`Groups.ParentMethods.group_generators`.

            EXAMPLES::

                sage: W = ColoredPermutations(3,2)
                sage: for gen in W.group_generators():
                ....:     print gen
                [[0, 0], [2, 1]]
                [[0, 1], [1, 2]]
            """
            return sorted(self.simple_reflections())

        semigroup_generators = group_generators

        def is_irreducible(self):
            r"""
            Return True if ``self`` is irreducible.

            EXAMPLES::

                sage: W = ColoredPermutations(1,3); W
                1-colored permutations of size 3
                sage: W.is_irreducible()
                True

                sage: W = ReflectionGroup((1,1,3),(2,1,3)); W
                Reducible complex reflection group of rank 5 and type A2 x B3
                sage: W.is_irreducible()
                False
            """
            return self.nr_irreducible_components() == 1

        def is_reducible(self):
            r"""
            Return ``True`` if ``self`` is not irreducible.

            EXAMPLES::

                sage: W = ColoredPermutations(1,3); W
                1-colored permutations of size 3
                sage: W.is_reducible()
                False

                sage: W = ReflectionGroup((1,1,3), (2,1,3)); W
                Reducible complex reflection group of rank 5 and type A2 x B3
                sage: W.is_reducible()
                True
            """
            return not self.is_irreducible()

    class ElementMethods:

        # at least one of the two methods must be reimplemented
        # it is recommended to reimplement both, as computing
        # the inverse might not be very efficient...

        def apply_simple_reflection_left(self, i):
            """
            Return ``self`` multiplied by the simple reflection ``s[i]``
            on the left.

            This low level method is used intensively. Coxeter groups
            are encouraged to override this straightforward
            implementation whenever a faster approach exists.

            EXAMPLES::

                sage: W = ComplexReflectionGroups().example()
                sage: w = W.an_element(); w
                [[1, 0, 0], [3, 1, 2]]
                sage: w.apply_simple_reflection_left(1)
                [[0, 1, 0], [1, 3, 2]]
                sage: w.apply_simple_reflection_left(2)
                [[1, 0, 0], [3, 2, 1]]
                sage: w.apply_simple_reflection_left(3)
                [[1, 0, 1], [3, 1, 2]]
            """
            s = self.parent().simple_reflections()
            return s[i] * self

        def apply_simple_reflection_right(self, i):
            """
            Return ``self`` multiplied by the simple reflection ``s[i]``
            on the right.

            This low level method is used intensively. Coxeter groups
            are encouraged to override this straightforward
            implementation whenever a faster approach exists.

            EXAMPLES::

                sage: W = ComplexReflectionGroups().example()
                sage: w = W.an_element(); w
                [[1, 0, 0], [3, 1, 2]]
                sage: w.apply_simple_reflection_right(1)
                [[1, 0, 0], [3, 2, 1]]
                sage: w.apply_simple_reflection_right(2)
                [[1, 0, 0], [2, 1, 3]]
                sage: w.apply_simple_reflection_right(3)
                [[2, 0, 0], [3, 1, 2]]
            """
            s = self.parent().simple_reflections()
            return self * s[i]

        def apply_simple_reflection(self, i, side = 'right'):
            """
            Return ``self`` * ``s[i]``.

            INPUT:

            - ``i`` -- an element of the index set
            - ``side`` -- (default: ``"right"``) ``"left"`` or ``"right"``

            This default implementation simply calls
            :meth:`apply_simple_reflection_left` or
            :meth:`apply_simple_reflection_right`.

            EXAMPLES::

                sage: W = CoxeterGroups().example()
                sage: w = W.an_element(); w
                (1, 2, 3, 0)
                sage: w.apply_simple_reflection(0, side = "left")
                (0, 2, 3, 1)
                sage: w.apply_simple_reflection(1, side = "left")
                (2, 1, 3, 0)
                sage: w.apply_simple_reflection(2, side = "left")
                (1, 3, 2, 0)

                sage: w.apply_simple_reflection(0, side = "right")
                (2, 1, 3, 0)
                sage: w.apply_simple_reflection(1, side = "right")
                (1, 3, 2, 0)
                sage: w.apply_simple_reflection(2, side = "right")
                (1, 2, 0, 3)

            By default, ``side`` is "right"::

                sage: w.apply_simple_reflection(0)
                (2, 1, 3, 0)
            """
            if side == 'right':
                return self.apply_simple_reflection_right(i)
            else:
                return self.apply_simple_reflection_left(i)

        @abstract_method(optional=True)
        def reflection_length(self):
            r"""
            Return the reflection length of ``self``.

            This is the minimal length of a factorization of ``self``
            into reflections.

            EXAMPLES::

                sage: W = ColoredPermutations(1,2)
                sage: sorted([ t.reflection_length() for t in W ])
                [0, 1]

                sage: W = ColoredPermutations(2,2)
                sage: sorted([ t.reflection_length() for t in W ])
                [0, 1, 1, 1, 1, 2, 2, 2]

                sage: W = ColoredPermutations(3,2)
                sage: sorted([ t.reflection_length() for t in W ])
                [0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

                sage: W = ReflectionGroup((2,2,2))
                sage: sorted([ t.reflection_length() for t in W ])
                [0, 1, 1, 2]
            """

        def is_reflection(self):
            r"""
            Return ``True`` if ``self`` is a reflection.

            EXAMPLES::

                sage: W = ColoredPermutations(1,4); W
                1-colored permutations of size 4
                sage: [ t.is_reflection() for t in W.reflections() ]
                [True, True, True, True, True, True]
                sage: len( [ t for t in W.reflections() if t.is_reflection() ] )
                6

                sage: W = ColoredPermutations(2,3); W
                2-colored permutations of size 3
                sage: [ t.is_reflection() for t in W.reflections() ]
                [True, True, True, True, True, True, True, True, True]
                sage: len( [t for t in W.reflections() if t.is_reflection() ] )
                9
            """
            return self.reflection_length() == 1

        def apply_simple_reflections(self, word, side = 'right'):
            r"""
            Return the result of the (left/right) multiplication of
            ``word`` to ``self``.

            INPUT:

            - ``word`` -- a sequence of indices of reflections
            - ``side`` -- (default: ``'right'``) indicates multiplying
              from left or right

            EXAMPLES::

                sage: W = ColoredPermutations(1,3); W
                1-colored permutations of size 3
                sage: W.one().apply_simple_reflections([1])
                [[0, 0, 0], [2, 1, 3]]
                sage: W.one().apply_simple_reflections([2])
                [[0, 0, 0], [1, 3, 2]]
                sage: W.one().apply_simple_reflections([2,1])
                [[0, 0, 0], [2, 3, 1]]
                sage: W.one().apply_simple_reflections([1,2])
                [[0, 0, 0], [3, 1, 2]]
                sage: W.one().apply_simple_reflections([1,2,1])
                [[0, 0, 0], [3, 2, 1]]
                sage: W.one().apply_simple_reflections([1,2,1,2])
                [[0, 0, 0], [2, 3, 1]]
                sage: W.one().apply_simple_reflections([1,2,1,2,1])
                [[0, 0, 0], [1, 3, 2]]
                sage: W.one().apply_simple_reflections([1,2,1,2,1,2])
                [[0, 0, 0], [1, 2, 3]]
            """
            for i in word:
                self = self.apply_simple_reflection(i, side=side)
            return self

        def apply_distinguished_reflection(self, i, side = 'right'):
            r"""
            Return the result of the (left/right) multiplication of
            the ``i``-th distingiushed reflection to ``self``.

            INPUT:

            - ``i`` -- an index of a distinguished reflection
            - ``side`` -- (default: ``'right'``) multiplying from left/right

            EXAMPLES::

                sage: W = ColoredPermutations(1,3); W
                1-colored permutations of size 3
                sage: W.one().apply_distinguished_reflection(0)
                (1,4)(2,3)(5,6)
                sage: W.one().apply_distinguished_reflection(1)
                (1,3)(2,5)(4,6)
                sage: W.one().apply_distinguished_reflection(2)
                (1,5)(2,4)(3,6)

                sage: W = ColoredPermutations(1,3, hyperplane_index_set=['A','B','C']); W
                Irreducible complex reflection group of rank 2 and type A2
                sage: W.one().apply_distinguished_reflection('A')
                (1,4)(2,3)(5,6)
                sage: W.one().apply_distinguished_reflection('B')
                (1,3)(2,5)(4,6)
                sage: W.one().apply_distinguished_reflection('C')
                (1,5)(2,4)(3,6)
            """
            G = self.parent()
            if not i in G.hyperplane_index_set():
                raise ValueError("the given index %s is not an index of a hyperplane"%i)
            if side == 'right':
                return self * G.distinguished_reflection(i)
            else:
                return self.parent().reflection(i) * self

        def apply_distinguished_reflections(self, word, side='right'):
            r"""
            Return the result of the (left/right) multiplication of the
            distinguished reflections indexed by the elements in
            ``word`` to ``self``.

            INPUT:

             - ``word`` -- iterable of distinguished reflections indices
             - ``side`` -- (default: ``'right'``) multiplying from left/right

            EXAMPLES::

                sage: W = ColoredPermutations(1,3); W
                1-colored permutations of size 3
                sage: W.one().apply_distinguished_reflections([0])
                (1,4)(2,3)(5,6)
                sage: W.one().apply_distinguished_reflections([1])
                (1,3)(2,5)(4,6)
                sage: W.one().apply_distinguished_reflections([1,0])
                (1,2,6)(3,4,5)
            """
            for i in word:
                self = self.apply_distinguished_reflection(i, side=side)
            return self

        def apply_reflection(self, i, side='right'):
            r"""
            Return the result of the (left/right) multiplication of
            the ``i``-th reflection to ``self``.

            INPUT:

             - ``i`` -- an index of a reflection
             - ``side`` -- (default: ``'right'``) multiplying from left/right

            EXAMPLES::

                sage: W = ColoredPermutations(1,3); W
                1-colored permutations of size 3
                sage: W.one().apply_reflection(0)
                (1,4)(2,3)(5,6)
                sage: W.one().apply_reflection(1)
                (1,3)(2,5)(4,6)
                sage: W.one().apply_reflection(2)
                (1,5)(2,4)(3,6)

                sage: W = ColoredPermutations(1,3, reflection_index_set=['A','B','C']); W
                Irreducible complex reflection group of rank 2 and type A2
                sage: W.one().apply_reflection('A')
                (1,4)(2,3)(5,6)
                sage: W.one().apply_reflection('B')
                (1,3)(2,5)(4,6)
                sage: W.one().apply_reflection('C')
                (1,5)(2,4)(3,6)
            """
            W = self.parent()
            if i not in W.reflection_index_set():
                raise ValueError("the given index %s is not an index of a reflection"%i)
            if side == 'right':
                return self * W.reflection(i)
            else:
                return W.reflection(i) * self

        def apply_reflections(self, word, side='right'):
            r"""
            Return the result of the (left/right) multiplication of the
            reflections indexed by the elements in ``word`` to ``self``.

            INPUT:

             - ``word`` -- iterable of reflections indices
             - ``side`` -- (default: ``'right'``) multiplying from left/right

            EXAMPLES::

                sage: W = ColoredPermutations(1,3); W
                1-colored permutations of size 3
                sage: W.one().apply_reflections([0])
                (1,4)(2,3)(5,6)
                sage: W.one().apply_reflections([1])
                (1,3)(2,5)(4,6)
                sage: W.one().apply_reflections([1,0])
                (1,2,6)(3,4,5)
            """
            for i in word:
                self = self.apply_reflection(i, side=side)
            return self

    class Irreducible(CategoryWithAxiom):
        r"""
        The category of irreducible complex reflection groups.
        """
        class ParentMethods:
            def irreducible_components(self):
                r"""
                Return a list containing all irreducible components of
                ``self`` as finite reflection groups.

                EXAMPLES::

                    sage: W = ColoredPermutations(4, 3)
                    sage: W.irreducible_components()
                    [4-colored permutations of size 3]
                """
                return [self]

    class WellGenerated(CategoryWithAxiom):
        r"""
        The category of well-generated complex reflection groups.
        """
        class ParentMethods:
            def _test_well_generated(self, **options):
                """
                Check if ``self`` is well-generated.
                """
                tester = self._tester(**options)
                tester.assertEqual(self.nr_simple_reflections(), self.rank())

            def is_well_generated(self):
                r"""
                Return ``True`` as ``self`` is well-generated.
                """
                return True

    Finite = LazyImport('sage.categories.finite_complex_reflection_groups', 'FiniteComplexReflectionGroups')

