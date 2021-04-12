# 4.0 Introducción y Objetivos

Esta sección describe la metodología de pruebas de seguridad de la aplicación web de OWASP y explica cómo probar la evidencia de vulnerabilidades dentro de la aplicación debido a deficiencias en los controles de seguridad identificados.

## ¿Qué es la Prueba de Seguridad de Aplicaciones Web?

Una prueba de seguridad es un método de evaluación de la seguridad de un sistema o red informática mediante la validación y verificación metódica de la eficacia de los controles de seguridad de las aplicaciones. Una prueba de seguridad de aplicaciones web se centra únicamente en la evaluación de la seguridad de una aplicación web. El proceso implica un análisis activo de la aplicación para detectar cualquier debilidad, fallo técnico o vulnerabilidad. Cualquier problema de seguridad que se encuentre se presentará al propietario del sistema, junto con una evaluación del impacto, una propuesta de mitigación o una solución técnica.

## ¿Qué es una vulnerabilidad?

Una vulnerabilidad es un defecto o debilidad en el diseño, la aplicación, el funcionamiento o la gestión de un sistema que podría explotarse para comprometer los objetivos de seguridad del sistema.

## ¿Qué es una amenaza?

Una amenaza es cualquier cosa (un atacante externo malintencionado, un usuario interno, una inestabilidad del sistema, etc.) que pueda dañar los activos de una aplicación (recursos de valor, como los datos de una base de datos o del sistema de archivos) mediante la explotación de una vulnerabilidad.

## ¿Qué es una prueba?

Una prueba es una acción para demostrar que una aplicación cumple con los requisitos de seguridad de sus partes interesadas.

## El enfoque de esta guía

El enfoque de OWASP es abierto y colaborativo:

- Abierto: Todo experto en seguridad puede participar con su experiencia en el proyecto. Todo es gratis
- Colaborativo: se realiza una lluvia de ideas antes de escribir los artículos para que el equipo pueda compartir ideas y desarrollar una visión colectiva del proyecto. Eso significa un consenso aproximado, un público más amplio y una mayor participación.

Este enfoque tiende a crear una metodología de prueba definida que será:

- Consistente
- Reproducible
- Rigoroso
- Bajo control de calidad

Los problemas que deben abordarse están plenamente documentados y comprobados. Es importante utilizar un método para probar todas las vulnerabilidades conocidas y documentar todas las actividades de prueba de seguridad.

## ¿Qué es la metodología de prueba OWASP?

Las pruebas de seguridad nunca serán una ciencia exacta en la que se pueda definir una lista completa de todos los posibles problemas que deben ser probados. De hecho, la prueba de seguridad es sólo una técnica apropiada para probar la seguridad de las aplicaciones web en determinadas circunstancias. El objetivo de este proyecto es recopilar todas las técnicas de prueba posibles, explicar estas técnicas y mantener la guía actualizada. El método de Prueba de Seguridad de Aplicaciones Web de OWASP se basa en el enfoque de caja negra. El probador no sabe nada o tiene muy poca información sobre la aplicación a probar.

El modelo consta de:

- Tester (o probador): Quién realiza las actividades de prueba
- Herramienta y metodología: El núcleo de este Proyecto de Guía de Testeo/Prueba
- Aplicación: La caja negra para probar/testear

Las pruebas se pueden clasificar como pasivas o activas:

### Pruebas/Testeo pasivas

Durante las pruebas pasivas, un probador trata de entender la lógica de la aplicación y explora la aplicación como usuario. Se pueden utilizar herramientas para la recopilación de información. Por ejemplo, se puede utilizar un proxy HTTP para observar todas las solicitudes y respuestas HTTP. Al final de esta fase, el probador debe comprender en general todos los puntos de acceso y la funcionalidad del sistema (por ejemplo, los encabezados de HTTP, los parámetros, las cookies, las API, el uso y los patrones de tecnología, etc.). La sección [ de Recopilación de Información](../01-Information_Gathering/README.md) explica cómo realizar pruebas pasivas.

Por ejemplo, un probador puede encontrar una página en el siguiente URL: <code>https://www.example.com/login/auth_form</code>

Esto puede indicar un formulario de autenticación en el que la solicitud pide un nombre de usuario y una contraseña.

Los siguientes parámetros representan dos puntos de acceso a la aplicación: `https://www.example.com/appx?a=1&b=1`

En este caso, la aplicación muestra dos puntos de acceso (parametros `a` y `b`). Todos los puntos de acceso encontrados en esta fase representan un objetivo para la prueba. El seguimiento del directorio o árbol de llamadas de la aplicación y de todos los puntos de acceso puede ser útil durante las pruebas activas.

### Pruebas/Testeo activo

Durante las pruebas activas, el probador comienza a utilizar las metodologías descritas en las siguientes secciones.

El conjunto de pruebas activas se ha dividido en 12 categorías:

- Recopilación de Información
- Configuración y Pruebas de gestión e implementación
- Pruebas de gestión de identidad
- Pruebas de Autenticación
- Pruebas de Autorización
- Pruebas de gestión de sesiones
- Pruebas de validación de entrada
- Manejo de errores
- Criptografía
- Prueba de lógica de negocio
- Prueba del lado del cliente
- Pruebas de API
