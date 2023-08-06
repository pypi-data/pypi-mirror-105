(OOP\_school1235) Library For Learning OOP By RYU
=================================================

This Program is for my class about OOP

Download
~~~~~~~~

Open CMD / Terminal

.. code:: python

    pip install OOP_school1235

How to use
~~~~~~~~~~

-  

.. code:: python

    from OOP_school1235 import *
    allstudent = []

    teacher1 = Teacher('Ada')
    teacher2 = Teacher('Bill Gates')
    print(teacher1.students)


    # Day 1
    print('--- Day 1 ---') 
    st1 = Student('PonAek', 'JanOCha')
    allstudent.append(st1) # Register Finished then Save to List! Immediately
    print(st1.fullname)
    teacher2.AddStudent(st1)


    # Day 2
    print('--- Day 2 ---')
    st2 = Student('steve', 'Jobs')
    allstudent.append(st2)
    print(st2.fullname)
    teacher2.AddStudent(st2)


    # Day 3
    print('--- Day 3 ---')
    for i in range(3):
        st1.Coding()
    st2.Coding()
    st1.ShowExp()
    st2.ShowExp()

    # Day 4
    print('--- Day 4 ---')

    stp1 = SpecialStudent('Def', 'Editor', 'Pychoom')
    allstudent.append(stp1)
    print(stp1.fullname)
    print('Teacher, Can I take free some 20 exp')
    stp1.exp = 20 # Can edit values in Class
    stp1.Coding()
    stp1.ShowExp()
    teacher1.AddStudent(stp1)

    # Day 5
    print('--- Day 5 ---')
    print('Student How can you back to home?')
    print(allstudent)

    for st in allstudent:
        print(f'Me, {st.name} Back to home by {st.vehicle}.')
        if isinstance(st, SpecialStudent):
            st.vehicle.SelfDriving(st)

    # Day 6
    print('--- Day 6 ---')

    teacher1.CheckStudent()
    teacher2.CheckStudent()

    print('All Scores of Two Studet', st1+st2)

Develop By Ryu
