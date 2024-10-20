class Student:

    def __init__(self):
        self._age = None

    def get_age(self):
        print('获取属性时执行的代码')
        return self._age

    def set_age(self, age):
        print('设置属性时执行的代码')
        self._age = age

    def del_age(self):
        # print('删除属性时执行的代码')
        del self._age

    age = property(get_age, set_age, del_age, '学生年龄')



student = Student()
# 注意要用 类名.属性.__doc__ 的形式查看属性的文档字符串
print('查看属性的文档字符串：' + Student.age.__doc__)


# 设置属性
student.age = 28

# 获取属性
print('学生年龄为：' + str(student.age))

# 删除属性
del student.age
