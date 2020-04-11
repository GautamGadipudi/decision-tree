class Example:
    def __init__(
                self, 
                attributes,
                class_type
            ):  
                self.attributes = attributes
                self.class_type = class_type

    def __str__(self):
        return f'{self.attributes.__str__()} | {self.class_type}'