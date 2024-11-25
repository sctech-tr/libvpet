# `libvpet` - a virtual pet library
you want a pet? you have to code it >:)
## what's the purpose of this
I don't like existing virtual pet services, so I made my own. libvpet's goal is to be realistic as possible. you have to feed, play, and take care of your pet. if you don't, your pet will be sad :(
## how to use
```python
from libvpet import VirtualPet
pet = libvpet.VirtualPet("./cutedoggo.json", name="cutedoggo")

# feed your pet
pet.feed()

# play with your pet
pet.play()

# sleep your pet
pet.sleep()

# view status of your pet
pet.status()

# age your pet
pet.age_pet()
```
## competition
I will be hosting a competition to see who can implement a web version of this using libvpet. the winner will get a shoutout here. good luck! open an issue to submit your project.
