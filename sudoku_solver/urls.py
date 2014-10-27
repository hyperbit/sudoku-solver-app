from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sudoku_solver.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', include('sudoku.urls', namespace="sudoku")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/', include('sudoku.urls', namespace="sudoku")),
)
