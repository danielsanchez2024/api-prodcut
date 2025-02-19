Necesitamos que cree un microservicio de python que haga uso de las siguientes bases de datos:
- MongoDB
- Elasticsearch
- Redis

Crear un proyecto siguiendo la Arquitectura de kustomize donde:
- Se dockeriza el servicio de Backend con python y se debe dejar los manifiestos para el despliegue en el folder correspondiente a la arquitectura (es obligatorio para le funcionamiento de la app)
- Se crean los manifiestos para desplegar las diferentes bases de datos con helm desde su directorio inicial
- Se crean los manifiestos para el despliegue de un nuevo componente opcional que no es indispensable en cada entornos (los servicios son metabase y postgres en el componente de analítica)
- Se usa helm para el despliegue de un controlador de ingress (nginx) con helm
- El servicio de backoffice debe tener un ingress con el host python.gopenux.lan en la ruta /
- Las bases de datos deben tener volumenes persistentes
- Los certificados SSL deben soportar cualquier subdominio del dominio gopenux.lan y se debe agregar el ssl a los ingress como un secreto (obviando el tipo de secreto usado)
- El backend debe llevar una variable de entorno "NAMESPACE" que equivale al label del namespace en el que está
- Cada componente separado debe estar en un namespace diferente el cual se conforma por "gopenux-$nombre_componente-$entorno-ns"
- Se deben tener 3 entornos (Canary, Preproducción y Producción) los cuales deben despelgar los siguientes componentes:
    - Canary: Backend, bases de datos, controlador del ingress (el dominio se debe cambiar a python-canary.gopenux.lan con patches)
    - Preproducción: Backend, bases de datos, controlador del ingress (el dominio se debe cambiar a python-pre.gopenux.lan con patches) y metabase con su postgres para el funcionamiento (con un ingress en el host metabase-pre.gopenux.lan)
    - Producción: Backend, bases de datos, controlador del ingress (el dominio se debe cambiar a python.gopenux.lan con patches) y metabase con su postgres para el funcionamiento (con un ingress en el host metabase.gopenux.lan)

### Cosas a tener en cuenta
- La conexión a las bases de datos se hace mediante variables de entorno con una conexión interna
- Las imagenes deben estar en el registry de docker hub con un repo privado, por lo que cada componente debe tener un secreto con las credenciales del registry para la descarag de la imagen)
- Cada entorno debe desplegarse en un clúster de minikube con al menos 2 nodos
- Dependiendo del entorno, se deben agregar los limites de recursos teniendo en cuenta que canary es para pruebas, pre debe ser muy parecido a pro y pro es el más usado
- Usar la mayor cantidad de etiquetas de kustomize posible