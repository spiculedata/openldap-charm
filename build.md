# Charm building

    charm build .
    charm push /home/stephen/projects/charms/builds/openldap cs:~spiculecharms/openldap
    charm release ~spiculecharms/openldap-$version


# Source code

    git add *
    git commit -a -m "my message"
    git push
