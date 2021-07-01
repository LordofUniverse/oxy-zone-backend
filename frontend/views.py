from django.db.models import query
from django.http.response import Http404
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import Sellers, Places
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

import bcrypt

from frontend import serializers

# Create your views here.

class PlacesView(viewsets.ModelViewSet):
    serializer_class = PlacesSerializer
    queryset = Places.objects.all()

class PlaceswithemailnameView(APIView):

    def get(self, request, format=None):

        queryset = Places.objects.filter().values()

        final = []
        
        for i in queryset:
            newquery = Sellers.objects.get(id = int(i['foreign_seller_id']))

            newob = i
            newob['name'] = newquery.name
            newob['email'] = newquery.email
            newob['desc'] = newquery.desc
            newob['profilephoto'] = str(newquery.profilephoto)
            final.append(newob)

        return Response({'Data': final}, status=status.HTTP_201_CREATED)

    

class SellersView(viewsets.ModelViewSet):
    serializer_class = SellersSerializer
    queryset = Sellers.objects.only('id', 'name', 'email' )

class SellersLoginView(APIView):
    serializer_class = SellersLoginSerializer


    def post(self, request, format=None):


        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            emai = serializer.data.get('email')
            pwd = serializer.data.get('password')
            condition = serializer.data.get('condition')

            loginqueryset = Sellers.objects.filter(email = emai, password = pwd)

            if loginqueryset.exists():

                    room = Sellers.objects.get(email = emai, password = pwd)
                    hashed = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt(16))

                    
                    d = SellersLoginwithimgandpwdSerializer(room).data
                    d['password'] = hashed

                    return Response({'Data': d}, status=status.HTTP_201_CREATED)

            else:
                return Response({'msg': 'It doesnt exists.'}, status=status.HTTP_226_IM_USED )
                    
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class SellersSignupView(APIView):
    serializer_class = SellersSignupSerializer

    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            nam = serializer.data.get('name')
            emai = serializer.data.get('email')
            pwd = serializer.data.get('password')
            condition = serializer.data.get('condition')

            signupqueryset = Sellers.objects.filter(email = emai)
                
            if signupqueryset.exists():
                    
                return Response({'msg': 'It already exists.'}, status=status.HTTP_226_IM_USED)

            else:

                room = Sellers(name = nam, email = emai, password = pwd)
                room.save()
                
                return Response({'Data' : 'succesfuly created'}, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class SellersdetailsView(APIView):

    serializer_class = SellersDetailsSerializer

    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            id = serializer.data.get('id')
            name = serializer.data.get('name')
            email = serializer.data.get('email')
            password = serializer.data.get('password')

            sellerqueryset = Sellers.objects.filter(id = id, email = email, name = name)
                
            if sellerqueryset.exists():

                sellerquerydata = Sellers.objects.get(id = id, email = email, name = name)

                # if bcrypt.checkpw(sellerquerydata.password.encode('utf-8'), password.encode('utf-8')):
                #     print("It Matches!")

                placedata = Places.objects.filter(foreign_seller = sellerquerydata)
                count = placedata.count()

                if count != 0:

                    result_serializer = PlacesSerializer(placedata, many = True)

                    return Response({'Data': result_serializer.data}, status= status.HTTP_200_OK)

                else:
                    return Response({'Data': 'No data'}, status = status.HTTP_226_IM_USED)

            return Response({'Data': 'Id itself is wrong'}, status = status.HTTP_226_IM_USED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)     

class SellersdeleteView(APIView):
    
    serializer_class = PlacesdeleteSerializer

    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            id = serializer.data.get('id')
            location = serializer.data.get('location')
            addr = serializer.data.get('addr')
            phno = serializer.data.get('phno')
            oxyprice = serializer.data.get('oxyprice')

            sellerqueryset = Sellers.objects.filter(id = id)

            if sellerqueryset.exists():

                sellerdata = Sellers.objects.get(id = id)

                placequerydata = Places.objects.filter(foreign_seller = sellerdata, location = location, addr = addr, phno = phno, oxyprice = oxyprice)

                count = placequerydata.count()

                if count != 0:

                    placequerydata.delete()

                    return Response({'Data': 'successfully deleted'}, status= status.HTTP_200_OK)

                else:
                    return Response({'Data': 'No data'}, status = status.HTTP_226_IM_USED)

            return Response({'Data': 'Id itself is wrong'}, status = status.HTTP_226_IM_USED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)      

class SellerssaveoldView(APIView):
    
    serializer_class = PlacessaveoldSerializer

    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            id = serializer.data.get('id')
            location = serializer.data.get('location')
            addr = serializer.data.get('addr')
            phno = serializer.data.get('phno')
            oxyprice = serializer.data.get('oxyprice')
            oldlocation = serializer.data.get('oldlocation')
            oldaddr = serializer.data.get('oldaddr')
            oldphno = serializer.data.get('oldphno')
            oldoxyprice = serializer.data.get('oldoxyprice')

            sellerqueryset = Sellers.objects.filter(id = id)

            if sellerqueryset.exists():

                sellerdata = Sellers.objects.get(id = id)

                placequerydata = Places.objects.filter(foreign_seller = sellerdata, location = oldlocation, addr = oldaddr, phno = oldphno, oxyprice = oldoxyprice)

                count = placequerydata.count()

                if count != 0:

                    placequerydata.update(location = location, phno = phno, addr = addr, oxyprice = oxyprice)

                    result_serializer = PlacesSerializer(placequerydata, many = True)

                    return Response({'Data': 'Saved data'}, status= status.HTTP_200_OK)

                else:
                    return Response({'Data': 'No data'}, status = status.HTTP_226_IM_USED)

            return Response({'Data': 'Id itself is wrong'}, status = status.HTTP_226_IM_USED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)      

class SellerssavenewView(APIView):
    
    serializer_class = PlacessavenewSerializer

    def post(self, request, format=None):

        print('data: ', request.data)

        serializer = self.serializer_class(data=request.data)

        print('serializer', serializer)

        print(request.data['phno'], type(request.data['phno']))
        print(request.data['oxyprice'], type(request.data['oxyprice']))
        print(request.data['id'], type(request.data['id']))

        #if serializer.is_valid():

        if type(request.data['phno']) == int and type(request.data['oxyprice']) == float and type(request.data['id']) == int and type(request.data['location']) == str and type(request.data['addr']) == str:

            print('huh, valid')
            
            #id = serializer.data.get('id')
            #location = serializer.data.get('location')
            #addr = serializer.data.get('addr')
            #phno = serializer.data.get('phno')
            #oxyprice = serializer.data.get('oxyprice')

            id = request.data['id']
            location = request.data['location']
            addr = request.data['addr']
            phno = request.data['phno']
            oxyprice = request.data['oxyprice']

            sellerqueryset = Sellers.objects.filter(id = id)

            print('sellerqueryset:', sellerqueryset.values())

            if sellerqueryset.exists():

                print('exists')

                sellerdata = Sellers.objects.get(id = id)

                print('sellerdata:', sellerdata)

                placequerydata = Places(foreign_seller = sellerdata, location = location, addr = addr, phno = phno, oxyprice = oxyprice)

                print('before save: ', placequerydata)
                
                placequerydata.save()

                return Response({'Data': 'Saved data'}, status = status.HTTP_200_OK)

            return Response({'Data': 'Id itself is wrong'}, status = status.HTTP_226_IM_USED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)  

     
class Sellersdetailsbyid(APIView):
    
    serializer_class = SellersidSerializer

    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            id = serializer.data.get('id')

            sellerqueryset = Sellers.objects.filter(id = id)

            if sellerqueryset.exists():

                sellerdata = Sellers.objects.get(id = id)

                returnserializer = SellersnameemailSerializer(sellerdata)

                return Response(returnserializer.data, status = status.HTTP_200_OK)

            return Response({'Data': 'Id itself is wrong'}, status = status.HTTP_226_IM_USED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)  


class SellersUpdateView(APIView):
    
    serializer_class = SellersupdatedetailsSerializer

    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            id = serializer.data.get('id')
            name = serializer.data.get('name')
            email = serializer.data.get('email')
            oldname = serializer.data.get('oldname')
            oldemail = serializer.data.get('oldemail')
            cond = serializer.data.get('cond')
            cond2 = serializer.data.get('cond2')
            oldp = serializer.data.get('oldpassword')
            newp = serializer.data.get('newpassword')
            photo = serializer.data.get('profilephoto')
            desc = serializer.data.get('desc')

            if cond == 'yes': #password too going to be changed
                
                sellerqueryset = Sellers.objects.filter(id = id, name = oldname, email = oldemail, password = oldp)

                if sellerqueryset.exists():

                    if cond2 == 'yes': #including profile photo

                        sellerqueryset = Sellers.objects.get(id = id, name = oldname, email = oldemail, password = oldp)

                        if oldemail != email:
                            checkdata = Sellers.objects.filter(email = email)

                            if checkdata.exists():
                                return Response({'Data': 'Email exists'}, status = status.HTTP_226_IM_USED)

                            else:

                                sellerqueryset.name = name
                                sellerqueryset.email = email
                                if desc != None and desc != '': 
                                    sellerqueryset.desc = desc
                                sellerqueryset.password = newp
                                sellerqueryset.profilephoto = request.FILES['profilephoto']
                                sellerqueryset.save()

                                pwd = sellerqueryset.password.encode('utf-8')
                                hashed = bcrypt.hashpw(pwd, bcrypt.gensalt(16))

                                return Response({'Data': [str(sellerqueryset.profilephoto), hashed]}, status = status.HTTP_200_OK)

                        else:

                            sellerqueryset.name = name
                            sellerqueryset.email = email
                            if desc != None and desc != '': 
                                sellerqueryset.desc = desc
                            sellerqueryset.password = newp
                            sellerqueryset.profilephoto = request.FILES['profilephoto']
                            sellerqueryset.save()

                            pwd = sellerqueryset.password.encode('utf-8')
                            hashed = bcrypt.hashpw(pwd, bcrypt.gensalt(16))

                            return Response({'Data': [str(sellerqueryset.profilephoto), hashed]}, status = status.HTTP_200_OK)

                    else: #no update on profile photo

                        sellerqueryset = Sellers.objects.get(id = id, name = oldname, email = oldemail, password = oldp)

                        #check if new email new one exsts -> point is -> email is unique.... password, name, desc, photo, can be same

                        if oldemail != email:
                            checkdata = Sellers.objects.filter(email = email)

                            if checkdata.exists():
                                return Response({'Data': 'Email exists'}, status = status.HTTP_226_IM_USED)

                            else:

                                sellerqueryset.name = name
                                sellerqueryset.email = email
                                if desc != None and desc != '': 
                                    sellerqueryset.desc = desc
                                sellerqueryset.password = newp
                                sellerqueryset.save()

                                pwd = sellerqueryset.password.encode('utf-8')
                                hashed = bcrypt.hashpw(pwd, bcrypt.gensalt(16))

                                return Response({'Data': [str(sellerqueryset.profilephoto), hashed]}, status = status.HTTP_200_OK)

                        else:
                            sellerqueryset.name = name
                            sellerqueryset.email = email
                            if desc != None and desc != '': 
                                sellerqueryset.desc = desc
                            sellerqueryset.password = newp
                            sellerqueryset.save()

                            pwd = sellerqueryset.password.encode('utf-8')
                            hashed = bcrypt.hashpw(pwd, bcrypt.gensalt(16))

                            return Response({'Data': [str(sellerqueryset.profilephoto), hashed]}, status = status.HTTP_200_OK)

                else:
                    return Response({'Data': 'Id itself is wrong'}, status = status.HTTP_226_IM_USED)



            elif cond == 'no': #password not to be changed

                sellerqueryset = Sellers.objects.filter(id = id, name = oldname, email = oldemail)

                if sellerqueryset.exists():

                    if cond2 == 'yes': #change in profile photo too

                        sellerqueryset = Sellers.objects.get(id = id, name = oldname, email = oldemail)

                        if oldemail != email:
                            checkdata = Sellers.objects.filter(email = email)

                            if checkdata.exists():
                                return Response({'Data': 'Email exists'}, status = status.HTTP_226_IM_USED)

                            else:

                                sellerqueryset.name = name
                                sellerqueryset.email = email
                                if desc != None and desc != '': 
                                    sellerqueryset.desc = desc
                                sellerqueryset.profilephoto = request.FILES['profilephoto']
                                sellerqueryset.save()

                                pwd = sellerqueryset.password.encode('utf-8')
                                hashed = bcrypt.hashpw(pwd, bcrypt.gensalt(16))

                                return Response({'Data': [str(sellerqueryset.profilephoto), hashed]}, status = status.HTTP_200_OK)

                        else:

                            sellerqueryset.name = name
                            sellerqueryset.email = email
                            if desc != None and desc != '': 
                                sellerqueryset.desc = desc
                            sellerqueryset.profilephoto = request.FILES['profilephoto']
                            sellerqueryset.save()

                            pwd = sellerqueryset.password.encode('utf-8')
                            hashed = bcrypt.hashpw(pwd, bcrypt.gensalt(16))

                            return Response({'Data': [str(sellerqueryset.profilephoto), hashed]}, status = status.HTTP_200_OK)

                    else: #no change in profile photo

                        sellerqueryset = Sellers.objects.get(id = id, name = oldname, email = oldemail)

                        if oldemail != email:
                            checkdata = Sellers.objects.filter(email = email)

                            if checkdata.exists():
                                return Response({'Data': 'Email exists'}, status = status.HTTP_226_IM_USED)

                            else:

                                sellerqueryset.name = name
                                sellerqueryset.email = email
                                if desc != None and desc != '': 
                                    sellerqueryset.desc = desc
                                sellerqueryset.save()

                                pwd = sellerqueryset.password.encode('utf-8')
                                hashed = bcrypt.hashpw(pwd, bcrypt.gensalt(16))

                                return Response({'Data': [str(sellerqueryset.profilephoto), hashed]}, status = status.HTTP_200_OK)

                        else:

                            sellerqueryset = Sellers.objects.get(id = id, name = oldname, email = oldemail)

                            sellerqueryset.name = name
                            sellerqueryset.email = email
                            if desc != None and desc != '': 
                                sellerqueryset.desc = desc
                            sellerqueryset.save()

                            pwd = sellerqueryset.password.encode('utf-8')
                            hashed = bcrypt.hashpw(pwd, bcrypt.gensalt(16))

                            return Response({'Data': [str(sellerqueryset.profilephoto), hashed]}, status = status.HTTP_200_OK)

                else:
                    return Response({'Data': 'Id itself is wrong'}, status = status.HTTP_226_IM_USED)

            else:
                return Response({'Data': 'condtion type wrong'}, status = status.HTTP_226_IM_USED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)      

class Sellersdetails2(APIView):
    
    serializer_class = Sellersdetails2Serializer

    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.data.get('email')

            sellerdetailsset = Sellers.objects.filter(email = email)

            if sellerdetailsset.exists():
                
                data = Sellers.objects.get(email = email)

                outputdata = Sellersdetails3Serializer(data).data

                return Response({'Data': outputdata}, status = status.HTTP_226_IM_USED)

            else:

                return Response({'Data': 'Email Wrong'}, status = status.HTTP_226_IM_USED)

        else:
            return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

