program calor

    implicit none

    double precision, dimension(:,:), allocatable :: u
    double precision :: mu, dx, dt
    integer :: l, n, d, Nfim, k

    mu = 0.5d0

    open(unit=1234, file='ordem_calor.dat', status='unknown')

    do k = 4,8

        dx = (1.d0/2.d0)**k
        d = int(1.d0/dx) - 1

        dt = mu * dx * dx
        Nfim = int(1.d0/dt)

        ! write(*,*) d, dx, Nfim, dt

        allocate(u(0:d+1, 0:Nfim))

        !! condição inicial
        do l = 0,d+1
            u(l,0) = dsin( acos(-1.d0) * l * dx )
        end do

        !! método de Euler explícito
        do n = 0,Nfim-1
            
            u(0,n+1) = p1((n+1) * dt) !! atualização da CC à esquerda
            u(d+1,n+1) = p2((n+1) * dt) !! atualizaçõa da CC à direita

            do l = 1,d !! laço no espaçø
                u(l,n+1) = u(l,n) + mu*( u(l+1,n) - 2.d0*u(l,n) + u(l-1,n) )
            end do
        end do

        write(1234,*) dx, dt*Nfim, Nfim, dabs(u((d+1)/2, Nfim) - dexp(-acos(-1.d0)*acos(-1.d0)))

        ! open(unit=123, file='saida_calor.dat', status='unknown')

        ! do n = 0,Nfim
        !     do l = 0,d+1
        !         write(123,*) n, l*dx, u(l,n), dexp(-acos(-1.d0)*acos(-1.d0)*n*dt)*dsin(acos(-1.d0)*l*dx)
        !     end do
        !     write(123,*) '   ' !! linha vazia entre dois blocos para plotar no gnuplot
        ! end do

        ! close(unit=123)

        deallocate(u)

    end do

    close(unit=1234)

contains

    function p1(t)

        implicit none

        double precision :: t, p1

        p1 = 0.d0

        return

    end function p1


    function p2(t)

        implicit none

        double precision :: t, p2

        p2 = 0.d0

        return

    end function p2

end program
