from django.shortcuts import get_object_or_404

class MultiSlugMixin(object):
    model = None
    def get_object(self, *args, **kwargs):
        print self.kwargs
        slug = self.kwargs.get("slug")
        print slug
        ModelClass = self.model
        if slug is not None:
            try:
                #producto = get_object_or_404(Producto, slug=slug)
                obj = get_object_or_404(ModelClass, slug=slug)
            except:
                #producto = Producto.objects.filter(slug=slug).order_by("-nombre").first()
                obj = ModelClass.objects.filter(slug=slug).order_by("-nombre").first()
        else:
            obj = super(MultiSlugMixin, self).get_object(*args, **kwargs)

        return obj
