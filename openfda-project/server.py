
import http.server
import socketserver
import json
import requests
# -- IP and the port of the server
IP = "127.0.0.1"  # Localhost means "I": your local machine
PORT = 8000




def company(companies,limit_search_companies):
    url = "https://api.fda.gov/drug/label.json?search=openfda.manufacturer_name:" + companies + "&limit=" + str(limit_search_companies)

    lista_companies = []
    limit = limit_search_companies
    i = 0
    repetir = True


    while repetir:
        try:
            url = "https://api.fda.gov/drug/label.json?search=openfda.manufacturer_name:" + companies + "&limit=" + str(limit)
            data = requests.get(url).json()
            for i in range(0,int(limit)):
                companies = data["results"][i]["openfda"]["manufacturer_name"]
                lista_companies.append(companies)
            mensaje = 'A continuacion aparece un listado de empresas que tienen alguna relacion con la que ha introducido:  '


            repetir = False
            return mensaje,lista_companies

        except IndexError:
            break
        except KeyError:

            mensaje = 'La empresa que acabas de buscar no esta incluida en el campo openfda.manufacturer_name.   '
            lista_companies.append('Sin resultados')
            return mensaje,lista_companies
            break

##############################################################################################################################################

def get_medicamento_active_ingredient(ingrediente_activo,limit_search_active_ingredient):

    url = "https://api.fda.gov/drug/label.json?search=active_ingredient:" + ingrediente_activo + "&limit=" + str(limit_search_active_ingredient)

    lista_medicamentos = []

    limit = limit_search_active_ingredient

    a = 0
    repetir = True
    while repetir:
        try:
            url = "https://api.fda.gov/drug/label.json?search=active_ingredient:" + ingrediente_activo + "&limit=" + str(limit)
            data = requests.get(url).json()

            for i in range(a,int(limit) + 1):
                medicamentos = data["results"][i]["openfda"]["generic_name"]
                lista_medicamentos.append(medicamentos)

            repetir = False
        except IndexError:
            break
        except KeyError:

            a = i + 1
            limit = limit + 1
            repetir = True


    if len(lista_medicamentos) == 0:
        mensaje = "Lo sentimos, no existe ningun farmaco con ese nombre en nuestra base de datos   :"
        lista_medicamentos.append('Sin resultados.')
        return mensaje,lista_medicamentos

    elif len(lista_medicamentos) == limit_search_active_ingredient:
        mensaje = 'A continuacion aparece un listado de medicamentos que poseen el ingrediente activo que ha introducido:'

        return mensaje,lista_medicamentos
###########################################################################################################################################
def get_drugs(limit_list_drugs):#Fármacos que serán finalmente introducidos en una lista
    url = "https://api.fda.gov/drug/label.json?search=openfda.product_type:ANIMAL COMPOUNDED DRUG LABEL&limit=" + str(limit_list_drugs)

    lista_drugs = []
    limit = limit_list_drugs
    repetir = True
    a = 0
    while repetir:
        try:
            url = "https://api.fda.gov/drug/label.json?search=openfda.product_type:ANIMAL COMPOUNDED DRUG LABEL&limit=" + str(limit)

            data = requests.get(url).json()
            for i in range(a,int(limit) + 1):
                drugs = data["results"][i]["openfda"]["generic_name"]
                lista_drugs.append(drugs)
            repetir = False

        except IndexError:
            break
        except KeyError:
            a = i + 1
            limit = limit + 1
            repetir = True
    mensaje = 'A continuacion aparece un listado de drogas provenientes de Openfda:  '
    return mensaje,lista_drugs

###############################################################################################################################################
#    return mensaje,lista_medicamentos
def get_list_companies(limit_list_companies):#las compañías que serán guardadas en una lista
    url = "https://api.fda.gov/drug/label.json?search=openfda.product_type:ANIMAL COMPOUNDED DRUG LABEL&limit=" + str(limit_list_companies)

    limit = limit_list_companies
    lista_companies = []
    repetir = True
    a = 0
    while repetir:
        try:
            url = "https://api.fda.gov/drug/label.json?search=openfda.product_type:ANIMAL COMPOUNDED DRUG LABEL&limit=" + str(limit)
            data = requests.get(url).json()
            for i in range(a,int(limit) + 1):
                companies = data["results"][i]["openfda"]["manufacturer_name"]
                lista_companies.append(companies)
            repetir = False

        except IndexError:
            break
        except KeyError:
            a = i + 1
            limit = limit + 1
            repetir = True
    mensaje = 'A continuacion aparece un listado de empresas que producen medicamentos a gran escala   :  '
    return mensaje,lista_companies
###########################################################################################################################

def get_warnings(limit_list_warnings):
    url = "https://api.fda.gov/drug/label.json?search=openfda.product_type:ANIMAL COMPOUNDED DRUG LABEL&limit=" + str(limit_list_warnings)


    lista_warnings = []

    limit = limit_list_warnings
    repetir = True
    a = 0

    while repetir:
        try:
            url = "https://api.fda.gov/drug/label.json?search=openfda.product_type:ANIMAL COMPOUNDED DRUG LABEL&limit=" + str(limit)
            data = requests.get(url).json()
            for i in range(a,int(limit) + 1):#Con este bucle obtenemos las advertencias de los fármacos.

                warnings = data["results"][i]["warnings"]
                lista_warnings.append(warnings)
            repetir = False
        except IndexError:
            break
        except KeyError:
            a = i + 1
            limit = limit + 1
            repetir = True

    mensaje = 'A continuacion aparece un listado de advertencias relacionada con la lista de medicamentos provenientes de Openfda   :'
    return mensaje,lista_warnings

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        list_submits = self.path.replace("/searchDrug?",'').replace("ingredient=",'').replace("name_company=",'').replace("limit",'').replace('&',',').replace('=','').split(',')
        print(list_submits)
#/action_page.php?active_ingredient=glycine&limit=0&name_company=bayer&limit=0&limit=0&limit=0&limit=0
        self.send_response(200)

        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if self.path[0:22] == "/searchDrug?ingredient":
            try:
                content_1 ="""
                    <!DOCTYPE html>
                    <html>
                    <link rel="icon" href="data:,">
                    <body style='background-color: #B955BD'>
                    <ul>
                    <li>"""

                content_2 = """
                    </li>
                    </ul>
                    </form>
                    </body>
                    </html>
                        """
            ######################################################################
                print(list_submits)
                ingrediente_activo = list_submits[0]
                limit_search_active_ingredient = int(list_submits[1])
                companies = list_submits[2]
                limit_search_companies = int(list_submits[3])
                limit_list_drugs = int(list_submits[4])
                limit_list_companies = list_submits[5]
                limit_list_warnings = int(list_submits[6])
            ######################################################################

                self.wfile.write(bytes('<br>',"utf-8"))
                self.wfile.write(bytes('<br>',"utf-8"))

            #############################################################################
                mensaje,lista_medicamentos = get_medicamento_active_ingredient(ingrediente_activo,limit_search_active_ingredient)

                self.wfile.write(bytes(mensaje,"utf-8"))

                for element in lista_medicamentos:
                    element = str(element)
                    content_definitivo_1 = content_1 + element + content_2
                    self.wfile.write(bytes(content_definitivo_1, "utf-8"))
            ##############################################################################

                self.wfile.write(bytes('<br>',"utf-8"))
                self.wfile.write(bytes('<br>',"utf-8"))

            #############################################################################
                mensaje, lista_companies = company(companies,limit_search_companies)
                self.wfile.write(bytes(mensaje,"utf-8"))

                for element in lista_companies:
                    element = str(element)
                    content_definitivo_2 = content_1 + element + content_2


                    self.wfile.write(bytes(content_definitivo_2, "utf-8"))
            ##############################################################################

                self.wfile.write(bytes('<br>',"utf-8"))
                self.wfile.write(bytes('<br>',"utf-8"))

            #############################################################################
                mensaje,lista_drugs = get_drugs(int(limit_list_drugs))

                self.wfile.write(bytes(mensaje, "utf-8"))

                for element in lista_drugs:
                    element = str(element)
                    content_definitivo_3 = content_1 + element + content_2


                    self.wfile.write(bytes(content_definitivo_3, "utf-8"))

            ##############################################################################

                self.wfile.write(bytes('<br>',"utf-8"))
                self.wfile.write(bytes('<br>',"utf-8"))

            #############################################################################
                mensaje,lista_companies = get_list_companies(int(limit_list_companies))

                self.wfile.write(bytes(mensaje, "utf-8"))

                for element in lista_companies:
                    element = str(element)
                    content_definitivo_4 = content_1 + element + content_2


                    self.wfile.write(bytes(content_definitivo_4, "utf-8"))
            ##############################################################################

                self.wfile.write(bytes('<br>',"utf-8"))
                self.wfile.write(bytes('<br>',"utf-8"))

            #############################################################################
                mensaje,lista_warnings = get_warnings(int(limit_list_warnings))

                self.wfile.write(bytes(mensaje, "utf-8"))

                for element in lista_warnings:
                    element = str(element)
                    content_definitivo_5 = content_1 + element + content_2

                    self.wfile.write(bytes(content_definitivo_5, "utf-8"))
            ##############################################################################

                    self.wfile.write(bytes('<br>',"utf-8"))
                    self.wfile.write(bytes('<br>',"utf-8"))
            except IndexError:
                a = True





        #print('imprime:',list_submits)
        elif self.path[0:11] == "/searchDrug": #Si me pides barra te envío...

            content_1 = """
                <!DOCTYPE html>
                <html>
                <link rel="icon" href="data:,">
                <body style='background-color: #65B41B'>
                <ul>
                <li>
                """
            content_2 = """
                </li>
                </ul>
                </form>
                </body>
                </html>
                """
            ingrediente_activo = self.path[29:]


            mensaje,lista_medicamentos = get_medicamento_active_ingredient(ingrediente_activo,limit_search_active_ingredient=10)

            self.wfile.write(bytes(mensaje,"utf-8"))
#############################################################################
            for element in lista_medicamentos:
                element = str(element)
                content_definitivo = content_1 + element + content_2


                self.wfile.write(bytes(content_definitivo, "utf-8"))
##############################################################################


        elif self.path[0:14] == '/searchCompany':
#/searchCompany?company=

            content_1 = """
                <!DOCTYPE html>
                <html>
                <link rel="icon" href="data:,">
                <body style='background-color: #1BB49A'>
                <ul>
                <li>
                """
            content_2 = """
                </li>
                </ul>
                </form>
                </body>
                </html>
                """
            limit_search_companies = 10
            companies = self.path[23:]

            mensaje, lista_companies = company(companies,limit_search_companies)
            self.wfile.write(bytes(mensaje,"utf-8"))
#############################################################################
            for element in lista_companies:
                element = str(element)
                content_definitivo = content_1 + element + content_2


                self.wfile.write(bytes(content_definitivo, "utf-8"))
##############################################################################


        elif self.path[0:10] == '/listDrugs':

            content_1 = """
                <!DOCTYPE html>
                <html>
                <link rel="icon" href="data:,">
                <body style='background-color: #B76DD5'>
                <ul>
                <li>
                """
            content_2 = """
                </li>
                </ul>
                </form>
                </body>
                </html>
                """



            try:
                limit_list_drugs = int(self.path[17:])
##############################################################################

                mensaje,lista_drugs = get_drugs(limit_list_drugs)

                self.wfile.write(bytes(mensaje, "utf-8"))
    #############################################################################
                for element in lista_drugs:
                    element = str(element)
                    content_definitivo = content_1 + element + content_2


                    self.wfile.write(bytes(content_definitivo, "utf-8"))
##############################################################################
            except ValueError:
                limit_list_drugs = '10'

                mensaje,lista_drugs = get_drugs(int(limit_list_drugs))

                self.wfile.write(bytes(mensaje, "utf-8"))
    #############################################################################
                for element in lista_drugs:
                    element = str(element)
                    content_definitivo = content_1 + element + content_2


                    self.wfile.write(bytes(content_definitivo, "utf-8"))


        elif self.path[0:14] == '/listCompanies':
            content_1 = """
                <!DOCTYPE html>
                <html>
                <link rel="icon" href="data:,">
                <body style='background-color: #B925BD'>
                <ul>
                <li>
                """
            content_2 = """
                </li>
                </ul>
                </form>
                </body>
                </html>
                """

            try:
                limit_list_companies = int(self.path[21:])
##############################################################################

                mensaje,lista_companies = get_list_companies(limit_list_companies)

                self.wfile.write(bytes(mensaje, "utf-8"))
    #############################################################################
                for element in lista_companies:
                    element = str(element)
                    content_definitivo = content_1 + element + content_2


                    self.wfile.write(bytes(content_definitivo, "utf-8"))
##############################################################################
            except ValueError:
                limit_list_companies = '10'

                mensaje,lista_companies = get_list_companies(int(limit_list_companies))

                self.wfile.write(bytes(mensaje, "utf-8"))
    #############################################################################
                for element in lista_companies:
                    element = str(element)
                    content_definitivo = content_1 + element + content_2


                    self.wfile.write(bytes(content_definitivo, "utf-8"))



#/listCompanies?limit=10
        elif self.path[0:13] == '/listWarnings':
            content_1 = """
                <!DOCTYPE html>
                <html>
                <link rel="icon" href="data:,">
                <body style='background-color: #B955BD'>
                <ul>
                <li>"""

            content_2 = """
                </li>
                </ul>
                </form>
                </body>
                </html>
                    """

            try:

                limit_list_warnings = int(self.path[20:])
##############################################################################

                mensaje,lista_warnings = get_warnings(limit_list_warnings)

                self.wfile.write(bytes(mensaje, "utf-8"))
    #############################################################################
                for element in lista_warnings:
                    element = str(element)
                    content_definitivo = content_1 + element + content_2


                    self.wfile.write(bytes(content_definitivo, "utf-8"))
##############################################################################
            except ValueError:
                print('ey',self.path[20:])
                limit_list_warnings = '10'

                mensaje,lista_warnings = get_warnings(int(limit_list_warnings))

                self.wfile.write(bytes(mensaje, "utf-8"))
    #############################################################################
                for element in lista_warnings:
                    element = str(element)
                    content_definitivo = content_1 + element + content_2


                    self.wfile.write(bytes(content_definitivo, "utf-8"))



#/listWarnings?limit=10
        elif self.path.endswith('/'):

#<input type="text" name="respuesta_lista_medicamentos" value="True">
#<input type="text" name="respuesta_lista_empresa" value="">
#<input type="text" name="respuesta_lista_advertencias" value="">
            content = """
                <!DOCTYPE html>
                <html>
                <link rel="icon" href="data:,">
                <body style='background-color: #3B44AC'>
                <h2>Servidor de informacion farmaceutica</h2>
                <form action="searchDrug" method="get">
                Esta pagina le proporcionara varios formularios para que pueda buscar informacion sin problemas.<br>
                Elija entre las siguientes opciones:<br>
                <br>
                1)Busqueda de farmacos por su ingrediente activo.<br>
                <br>
                <ul>
                <li>Ingrediente activo:</li>
                </ul>
                <br>
                <input type="text" name="ingredient" value="">
                <br>
                <input type="submit" value="Submit">

                <br>
                <br>
                1.Limit_search:<br>
                <input type="text" name="limit" value="0">
                <br>
                <input type="submit" value="Submit">
                <br>
                <br>
                <form action="searchCompany" method="get">
                2)Busqueda de empresas que producen farmacos.<br>
                <br>
                <ul>
                <li>Empresa:</li>
                </ul>
                <br>
                <input type="text" name="name_company" value="">
                <br>
                <input type="submit" value="Submit">
                <br>
                <br>
                2.Limit_search:<br>
                <input type="text" name="limit" value="0">
                <br>
                <input type="submit" value="Submit">
                <br>
                <br>
                <ul>
                <form action="listDrugs" method="get">
                <li>Lista de medicamentos.</li>
                </ul>
                <br>
                <br>
                <br>
                3.Limit_search:<br>
                <input type="text" name="limit" value="0">
                <br>
                <input type="submit" value="Submit">
                <br>
                <br>
                <ul>
                <form action="listCompanies" method="get">
                <li>Lista de empresas:</li>
                </ul>
                <br>
                <br>
                <br>
                4.Limit_search:<br>
                <input type="text" name="limit" value="0">
                <br>
                <input type="submit" value="Submit">
                <br>
                <br>
                <ul>
                <form action="listWarnings" method="get">
                <li>Lista de advertencias:</li>
                </ul>
                <br>
                <br>
                <br>
                5.Limit_search:<br>
                <input type="text" name="limit" value="0">
                <br>
                <input type="submit" value="Submit">
                <br>
                <br>
                </form>
                </body>
                </html>
                """
        ###########################################################################################################
            self.wfile.write(bytes(content,"utf-8"))



        #            except IOError:
        #          self.send_error(404, 'file not found')
#Si la url que has introducido es válida ejecutará el código devolviendo un true.
#Si la url que has introducido es inválida no ejecutará el código e imprimirá el ERROR.
#Aquí dependiendo de la respuesta lanzaremos un mensaje de error o no.
########################################################################################################################

        return


Handler = testHTTPRequestHandler


httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)

try:
    httpd.serve_forever()

except KeyboardInterrupt:
        pass

httpd.server_close()
print("")
print("Server stopped!")
socketserver.TCPServer.allow_reuse_address = True
# https://github.com/joshmaker/simple-python-webserver/blob/master/server.py
