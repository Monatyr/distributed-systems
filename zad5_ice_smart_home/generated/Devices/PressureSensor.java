//
// Copyright (c) ZeroC, Inc. All rights reserved.
//
//
// Ice version 3.7.7
//
// <auto-generated>
//
// Generated from file `devices.ice'
//
// Warning: do not edit this file.
//
// </auto-generated>
//

package Devices;

public interface PressureSensor extends Sensor
{
    float getPressure(com.zeroc.Ice.Current current);

    /** @hidden */
    static final String[] _iceIds =
    {
        "::Devices::PressureSensor",
        "::Devices::Sensor",
        "::Ice::Object"
    };

    @Override
    default String[] ice_ids(com.zeroc.Ice.Current current)
    {
        return _iceIds;
    }

    @Override
    default String ice_id(com.zeroc.Ice.Current current)
    {
        return ice_staticId();
    }

    static String ice_staticId()
    {
        return "::Devices::PressureSensor";
    }

    /**
     * @hidden
     * @param obj -
     * @param inS -
     * @param current -
     * @return -
    **/
    static java.util.concurrent.CompletionStage<com.zeroc.Ice.OutputStream> _iceD_getPressure(PressureSensor obj, final com.zeroc.IceInternal.Incoming inS, com.zeroc.Ice.Current current)
    {
        com.zeroc.Ice.Object._iceCheckMode(null, current.mode);
        inS.readEmptyParams();
        float ret = obj.getPressure(current);
        com.zeroc.Ice.OutputStream ostr = inS.startWriteParams();
        ostr.writeFloat(ret);
        inS.endWriteParams(ostr);
        return inS.setResult(ostr);
    }

    /** @hidden */
    final static String[] _iceOps =
    {
        "getAllMeasurements",
        "getLuminousIntensity",
        "getPressure",
        "getTemp",
        "getTimeOfDay",
        "ice_id",
        "ice_ids",
        "ice_isA",
        "ice_ping",
        "makeMeasurements"
    };

    /** @hidden */
    @Override
    default java.util.concurrent.CompletionStage<com.zeroc.Ice.OutputStream> _iceDispatch(com.zeroc.IceInternal.Incoming in, com.zeroc.Ice.Current current)
        throws com.zeroc.Ice.UserException
    {
        int pos = java.util.Arrays.binarySearch(_iceOps, current.operation);
        if(pos < 0)
        {
            throw new com.zeroc.Ice.OperationNotExistException(current.id, current.facet, current.operation);
        }

        switch(pos)
        {
            case 0:
            {
                return Sensor._iceD_getAllMeasurements(this, in, current);
            }
            case 1:
            {
                return Sensor._iceD_getLuminousIntensity(this, in, current);
            }
            case 2:
            {
                return _iceD_getPressure(this, in, current);
            }
            case 3:
            {
                return Sensor._iceD_getTemp(this, in, current);
            }
            case 4:
            {
                return Sensor._iceD_getTimeOfDay(this, in, current);
            }
            case 5:
            {
                return com.zeroc.Ice.Object._iceD_ice_id(this, in, current);
            }
            case 6:
            {
                return com.zeroc.Ice.Object._iceD_ice_ids(this, in, current);
            }
            case 7:
            {
                return com.zeroc.Ice.Object._iceD_ice_isA(this, in, current);
            }
            case 8:
            {
                return com.zeroc.Ice.Object._iceD_ice_ping(this, in, current);
            }
            case 9:
            {
                return Sensor._iceD_makeMeasurements(this, in, current);
            }
        }

        assert(false);
        throw new com.zeroc.Ice.OperationNotExistException(current.id, current.facet, current.operation);
    }
}
