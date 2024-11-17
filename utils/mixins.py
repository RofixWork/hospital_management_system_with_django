from django.shortcuts import redirect
from django.urls import reverse_lazy


class RedirectAuthenticationUser:
    """
    Custom authentication backend for redirecting authenticated users to a specific URL
    """

    redirect_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(
                self.redirect_url
            )  # Redirect authenticated users to the home page
        return super().dispatch(request, *args, **kwargs)
