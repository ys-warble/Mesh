# Mesh

Mesh is an application that provides a model of 3-dimensional space with its content, including space factors and entities, for the purpose of simulating IoT interaction. Written in Python 3.

## Mesh's objectives:
* To establish a model of space in the form of space factors
* To form a model of entities with different types (light, air conditioner) and functionalities (sensing, actuating, computing)
* To model the interaction among entities and space factors
* To create and evaluate datasets in IoT research
* To help the research and development in pervasive computing

## Current Status: *Early Development*
Modules are actively being defined. Visualization is just enough for development, supported by Plotly, without optimization. Interface to the application has not been well-documented. However, the test cases show how to use with the application.
Supported entity:
* Light
* PowerSupply
* Switch

## Contact
Feel free to contact yosef.saputra@gmail.com for more information and questions related to this application.

## Terminology
### Space
3-dimensional space in the form of 3-dimensional array.

### Space Factor
Components in the space. They capture different aspects in a space, for example: matter type, temperature, air movement, luminosity.

### Entity
Single encapsulated body that may have its own context, preference, intent, and action. Entity includes IoT smart things and user.

<!--### Context-->
<!--_TODO define_-->

<!--### Preference-->
<!--_TODO define_-->

<!--### Intent-->
<!--_TODO define_-->

<!--### Action-->
<!--_TODO define_-->

## Resources
**GitHub:** https://github.com/yosefsaputra/Mesh
**Docker (Tests)**: 
