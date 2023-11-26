program trabalho_itens_1_2

    implicit none

    double precision, dimension(:,:), allocatable :: u
    double precision :: mu, dx, dt, q1
    integer :: l, n, d, Nfim

    mu = 0.5d0

    dx = (1.d0/2.d0)**4
    d = int(10.d0/dx) - 1

    dt = mu * dx * dx
    Nfim = int(1.d0/dt)

    write(*,*) d, dx, Nfim, dt

    allocate(u(0:d+1, 0:Nfim))

    q1 = 0.71d0

    !! initial condition
    do l = 0,d+1
        u(l,0) = f(0.d0)*dexp(-q1*l*dx)
    end do

    !! expicit Euler scheme
    do n = 0,Nfim-1
        
        u(0,n+1) = f((n+1) * dt) !! left boundary condition
        u(d+1,n+1) = p2((n+1) * dt) !! right boundary condition

        do l = 1,d
            u(l,n+1) = u(l,n) + mu*( u(l+1,n) - 2.d0*u(l,n) + u(l-1,n) )
        end do
    end do

    open(unit=123, file='output_1_2.dat', status='unknown')

    do n = 0,Nfim
        do l = 0,d+1
            write(123,*) n, l*dx, u(l,n)
        end do
        write(123,*) '   ' !! empty line between blocks for gnuplot plotting
    end do

    close(unit=123)

    deallocate(u)

contains

    function f(t)

        implicit none

        double precision :: t, f

        if ( (t.ge.0d0).and.(t.le.0.5d0) ) then
			f = -1 !! winter temperature
		else
			f = 1 !! summer temperature
		end if

        return

    end function f


    function p2(t)

        implicit none

        double precision :: t, p2

        p2 = 0.d0

        return

    end function p2

end program trabalho_itens_1_2
