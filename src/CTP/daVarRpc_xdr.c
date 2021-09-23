/*
 * Please do not edit this file.
 * It was generated using rpcgen.
 */

#include "daVarRpc.h"
#include <time.h>
#define _xdr_result xdr_result
#define _xdr_argument xdr_argument

bool_t
xdr_PNAME (XDR *xdrs, PNAME *objp)
{
	register int32_t *buf;

	 if (!xdr_string (xdrs, objp, ~0))
		 return FALSE;
	return TRUE;
}

bool_t
xdr_NAMELIST (XDR *xdrs, NAMELIST *objp)
{
	register int32_t *buf;

	 if (!xdr_array (xdrs, (char **)&objp->NAMELIST_val, (u_int *) &objp->NAMELIST_len, ~0,
		sizeof (PNAME), (xdrproc_t) xdr_PNAME))
		 return FALSE;
	return TRUE;
}

bool_t
xdr_any (XDR *xdrs, any *objp)
{
	register int32_t *buf;

	 if (!xdr_int (xdrs, &objp->valtype))
		 return FALSE;
	switch (objp->valtype) {
	case DAVARINT_RPC:
		 if (!xdr_array (xdrs, (char **)&objp->any_u.i.i_val, (u_int *) &objp->any_u.i.i_len, ~0,
			sizeof (int), (xdrproc_t) xdr_int))
			 return FALSE;
		break;
	case DAVARFLOAT_RPC:
		 if (!xdr_array (xdrs, (char **)&objp->any_u.r.r_val, (u_int *) &objp->any_u.r.r_len, ~0,
			sizeof (float), (xdrproc_t) xdr_float))
			 return FALSE;
		break;
	case DAVARDOUBLE_RPC:
		 if (!xdr_array (xdrs, (char **)&objp->any_u.d.d_val, (u_int *) &objp->any_u.d.d_len, ~0,
			sizeof (double), (xdrproc_t) xdr_double))
			 return FALSE;
		break;
	case DAVARSTRING_RPC:
		 if (!xdr_string (xdrs, &objp->any_u.s, ~0))
			 return FALSE;
		break;
	case DAVARERROR_RPC:
		 if (!xdr_int (xdrs, &objp->any_u.error))
			 return FALSE;
		break;
	default:
		break;
	}
	return TRUE;
}

bool_t
xdr_wany (XDR *xdrs, wany *objp)
{
	register int32_t *buf;

	 if (!xdr_PNAME (xdrs, &objp->name))
		 return FALSE;
	 if (!xdr_pointer (xdrs, (char **)&objp->val, sizeof (any), (xdrproc_t) xdr_any))
		 return FALSE;
	return TRUE;
}

bool_t
xdr_RVALLIST (XDR *xdrs, RVALLIST *objp)
{
	register int32_t *buf;

	 if (!xdr_array (xdrs, (char **)&objp->RVALLIST_val, (u_int *) &objp->RVALLIST_len, ~0,
		sizeof (any), (xdrproc_t) xdr_any))
		 return FALSE;
	return TRUE;
}

bool_t
xdr_WVALLIST (XDR *xdrs, WVALLIST *objp)
{
	register int32_t *buf;

	 if (!xdr_array (xdrs, (char **)&objp->WVALLIST_val, (u_int *) &objp->WVALLIST_len, ~0,
		sizeof (wany), (xdrproc_t) xdr_wany))
		 return FALSE;
	return TRUE;
}

bool_t
xdr_ERRLIST (XDR *xdrs, ERRLIST *objp)
{
	register int32_t *buf;

	 if (!xdr_array (xdrs, (char **)&objp->ERRLIST_val, (u_int *) &objp->ERRLIST_len, ~0,
		sizeof (int), (xdrproc_t) xdr_int))
		 return FALSE;
	return TRUE;
}

bool_t
xdr_TESTNAMELIST (XDR *xdrs, TESTNAMELIST *objp)
{
	register int32_t *buf;


	if (xdrs->x_op == XDR_ENCODE) {
		 if (!xdr_string (xdrs, &objp->test_condition, ~0))
			 return FALSE;
		buf = XDR_INLINE (xdrs, 4 * BYTES_PER_XDR_UNIT);
		if (buf == NULL) {
			 if (!xdr_int (xdrs, &objp->max_time_wait))
				 return FALSE;
			 if (!xdr_int (xdrs, &objp->max_event_wait))
				 return FALSE;
			 if (!xdr_int (xdrs, &objp->prog))
				 return FALSE;
			 if (!xdr_int (xdrs, &objp->vers))
				 return FALSE;

		} else {
		IXDR_PUT_LONG(buf, objp->max_time_wait);
		IXDR_PUT_LONG(buf, objp->max_event_wait);
		IXDR_PUT_LONG(buf, objp->prog);
		IXDR_PUT_LONG(buf, objp->vers);
		}
		 if (!xdr_pointer (xdrs, (char **)&objp->NAMELISTP, sizeof (NAMELIST), (xdrproc_t) xdr_NAMELIST))
			 return FALSE;
		return TRUE;
	} else if (xdrs->x_op == XDR_DECODE) {
		 if (!xdr_string (xdrs, &objp->test_condition, ~0))
			 return FALSE;
		buf = XDR_INLINE (xdrs, 4 * BYTES_PER_XDR_UNIT);
		if (buf == NULL) {
			 if (!xdr_int (xdrs, &objp->max_time_wait))
				 return FALSE;
			 if (!xdr_int (xdrs, &objp->max_event_wait))
				 return FALSE;
			 if (!xdr_int (xdrs, &objp->prog))
				 return FALSE;
			 if (!xdr_int (xdrs, &objp->vers))
				 return FALSE;

		} else {
		objp->max_time_wait = IXDR_GET_LONG(buf);
		objp->max_event_wait = IXDR_GET_LONG(buf);
		objp->prog = IXDR_GET_LONG(buf);
		objp->vers = IXDR_GET_LONG(buf);
		}
		 if (!xdr_pointer (xdrs, (char **)&objp->NAMELISTP, sizeof (NAMELIST), (xdrproc_t) xdr_NAMELIST))
			 return FALSE;
	 return TRUE;
	}

	 if (!xdr_string (xdrs, &objp->test_condition, ~0))
		 return FALSE;
	 if (!xdr_int (xdrs, &objp->max_time_wait))
		 return FALSE;
	 if (!xdr_int (xdrs, &objp->max_event_wait))
		 return FALSE;
	 if (!xdr_int (xdrs, &objp->prog))
		 return FALSE;
	 if (!xdr_int (xdrs, &objp->vers))
		 return FALSE;
	 if (!xdr_pointer (xdrs, (char **)&objp->NAMELISTP, sizeof (NAMELIST), (xdrproc_t) xdr_NAMELIST))
		 return FALSE;
	return TRUE;
}