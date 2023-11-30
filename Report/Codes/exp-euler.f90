program exp_euler

    implicit none

    double precision, dimension(:,:), allocatable :: u
    double precision :: mu, dx, dt, q1, kappa, length, T
    integer :: l, n, d, Nfim

    q1 = 0.71d0
    kappa = 6.3d0
    length = kappa**0.5d0

    length = 15.d0
    T = 1.d0
    d = 150 !1500 !600 !300 !150
    Nfim = 1260 !int(100*1260) !int(16*1260) !int(4*1260) !1260
    dx = length / d
    dt = T / Nfim

    mu = dt / (dx * dx)

    write(*,*) mu, d, dx, Nfim, dt

    allocate(u(0:d+1, 0:Nfim))

    !! initial condition
    do l = 0,d+1
        u(l,0) = f(0.d0)*dexp(-q1*l*dx)
    end do

    !! expicit Euler scheme
    do n = 0,Nfim-1
        
        u(0,n+1) = f((n+1) * dt) !! left boundary condition
        u(d+1,n+1) = p2((n+1) * dt) !! right boundary condition

        do l = 1,d
            u(l,n+1) = u(l,n) + kappa*mu*( u(l+1,n) - 2.d0*u(l,n) + u(l-1,n) )
        end do
    end do

    open(unit=123, file='exp-euler.dat', status='unknown')

    do n = 0,Nfim
        do l = 0,d+1
            write(123,*) n, l*dx, u(l,n)
        end do
        write(123,*) '   ' !! empty line between blocks for gnuplot plotting
    end do

    close(unit=123)

    !! esse trecho foi usado apenas para o cálculo da ordem
    !! recomendo comentar a escrita no arquivo antes de executar
    ! write(*,*) dx, 50*dx, Nfim, Nfim*dt, u(50, Nfim)
    ! write(*,*) dx, 100*dx, Nfim, Nfim*dt, u(100, Nfim)
    ! write(*,*) dx, 200*dx, Nfim, Nfim*dt, u(200, Nfim)
    ! write(*,*) dx, 500*dx, Nfim, Nfim*dt, u(500, Nfim)

    deallocate(u)

contains

    function f(t)

        implicit none

        double precision :: t, f

        if ( (t.ge.0d0).and.(t.le.0.5d0) ) then
			f = 1 !! winter temperature
		else
			f = 10 !! summer temperature
		end if

        return

    end function f


    function p2(t)

        implicit none

        double precision :: t, p2

        p2 = 0.d0

        return

    end function p2

end program exp_euler
