from concurrent import futures
import logging

import grpc
import EmployeeService_pb2
import EmployeeService_pb2_grpc

import const

empDB=[
 {
 'id':101,
 'name':'Saravanan S',
 'title':'Technical Leader',
 'salary': 2000.0
 },
 {
 'id':201,
 'name':'Rajkumar P',
 'title':'Sr Software Engineer',
 'salary': 1000.0
 }
 ]

class EmployeeServer(EmployeeService_pb2_grpc.EmployeeServiceServicer):

  def CreateEmployee(self, request, context):
    dat = {
    'id':request.id,
    'name':request.name,
    'title':request.title,
    'salary': 3000.0
    }
    empDB.append(dat)
    return EmployeeService_pb2.StatusReply(status='OK')

  def GetEmployeeDataFromID(self, request, context):
    usr = [ emp for emp in empDB if (emp['id'] == request.id) ] 
    return EmployeeService_pb2.EmployeeData(id=usr[0]['id'], name=usr[0]['name'], title=usr[0]['title'])

  def UpdateEmployeeTitle(self, request, context):
    usr = [ emp for emp in empDB if (emp['id'] == request.id) ]
    usr[0]['title'] = request.title
    return EmployeeService_pb2.StatusReply(status='OK')

  def DeleteEmployee(self, request, context):
    usr = [ emp for emp in empDB if (emp['id'] == request.id) ]
    if len(usr) == 0:
      return EmployeeService_pb2.StatusReply(status='NOK')

    empDB.remove(usr[0])
    return EmployeeService_pb2.StatusReply(status='OK')

  def ListAllEmployees(self, request, context):
    list = EmployeeService_pb2.EmployeeDataList()
    for item in empDB:
      emp_data = EmployeeService_pb2.EmployeeData(id=item['id'], name=item['name'], title=item['title']) 
      list.employee_data.append(emp_data)
    return list
  
  def GetEmployeeSalaryMean(self, request, context):
    salaries = list(map(lambda x: float(x['salary']), empDB))
    salaryMean = sum(salaries) / len(salaries)
    return EmployeeService_pb2.EmployeeSalaryMean(salaryMean=salaryMean)

  def RaiseEmployeeSalaryByPercentage(self, request, context):
    percentage = request.percentage
    for emp in empDB:
        emp['salary'] = str(float(emp['salary']) * (1 + (percentage/100)))
    return EmployeeService_pb2.StatusReply(status='OK')

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    EmployeeService_pb2_grpc.add_EmployeeServiceServicer_to_server(EmployeeServer(), server)
    server.add_insecure_port('[::]:'+const.PORT)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
