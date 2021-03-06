#!/usr/bin/env python

# Copyright (C) 2014-2017, Cyberhaven
# Copyright (C) 2017, Dependable Systems Laboratory, EPFL
# All rights reserved.
#
# Licensed under the Cyberhaven Research License Agreement.



import pprint

from common import extract


def get_info(pdb):
    ret = {
        'version': pdb.product_version,
        'checksum': pdb.checksum,
        'bits': pdb.bits,
        'IopDeleteDriver': pdb.get_function_address('IopDeleteDriver'),
        'KeBugCheck2': pdb.get_function_address('KeBugCheck2'),
        'KdDebuggerDataBlock': pdb.get_function_address('KdDebuggerDataBlock'),
        'KdCopyDataBlock': pdb.get_function_address('KdCopyDataBlock', True),
        'KdpDataBlockEncoded': pdb.get_function_address('KdpDataBlockEncoded', True),

        'PsActiveProcessHead': pdb.get_function_address('PsActiveProcessHead'),
        'PsLoadedModuleList': pdb.get_function_address('PsLoadedModuleList'),
        'PerfLogImageUnload': pdb.get_function_address('PerfLogImageUnload', True),
        'ObpCreateHandle': pdb.get_function_address('ObpCreateHandle'),
        'MmAccessFault': pdb.get_function_address('MmAccessFault'),

        '_EPROCESS_VadRoot': pdb.get_field_offset('_EPROCESS:VadRoot'),

        'NtAllocateVirtualMemory': pdb.get_function_address('NtAllocateVirtualMemory'),
        'NtFreeVirtualMemory': pdb.get_function_address('NtFreeVirtualMemory'),
        'NtProtectVirtualMemory': pdb.get_function_address('NtProtectVirtualMemory'),
        'NtMapViewOfSection': pdb.get_function_address('NtMapViewOfSection'),
        'NtUnmapViewOfSection': pdb.get_function_address('NtUnmapViewOfSection'),
        'MiUnmapViewOfSection': pdb.get_function_address('MiUnmapViewOfSection'),
        #'NtUnmapViewOfSectionEx': pdb.get_function_address('NtUnmapViewOfSectionEx'),

        'KiInitialPCR': pdb.get_function_address('KiInitialPCR', True),

        '_KPRCB_ProcessorState': pdb.get_field_offset('_KPRCB:ProcessorState'),

        '_EPROCESS_ActiveProcessLinks': pdb.get_field_offset('_EPROCESS:ActiveProcessLinks'),
        '_EPROCESS_ThreadListHead': pdb.get_field_offset('_EPROCESS:ThreadListHead'),
        '_EPROCESS_UniqueProcessId': pdb.get_field_offset('_EPROCESS:UniqueProcessId'),
        '_EPROCESS_CommitCharge': pdb.get_field_offset('_EPROCESS:CommitCharge'),
        '_EPROCESS_VirtualSize': pdb.get_field_offset('_EPROCESS:VirtualSize'),
        '_EPROCESS_PeakVirtualSize': pdb.get_field_offset('_EPROCESS:PeakVirtualSize'),
        '_EPROCESS_CommitChargePeak': pdb.get_field_offset('_EPROCESS:CommitChargePeak'),
        '_EPROCESS_ExitStatus': pdb.get_field_offset('_EPROCESS:ExitStatus'),
        '_ETHREAD_ThreadListEntry': pdb.get_field_offset('_ETHREAD:ThreadListEntry'),
        '_ETHREAD_Cid': pdb.get_field_offset('_ETHREAD:Cid'),

        '_KPRCB_CurrentThread': pdb.get_field_offset('_KPRCB:CurrentThread'),
        '_KPCR_Prcb': pdb.get_field_offset('_KPCR:Prcb'),
        '_KPCR_KdVersionBlock': pdb.get_field_offset('_KPCR:KdVersionBlock'),
        '_KTHREAD_StackBase': pdb.get_field_offset('_KTHREAD:StackBase'),
        '_KTHREAD_StackLimit': pdb.get_field_offset('_KTHREAD:StackLimit'),
        '_KTHREAD_Process': pdb.get_field_offset('_KTHREAD:Process'),
        '_KPRCB_DpcStack': pdb.get_field_offset('_KPRCB:DpcStack'),
    }

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(ret)

    process = pdb.get_field_offset('_KTHREAD:Process')
    if process is not None:
        ret['_KTHREAD_Process'] = process
    else:
        process = pdb.get_field_offset('_ETHREAD:ThreadsProcess')
        if process is None:
            raise RuntimeError('Could not find process field')
        ret['_KTHREAD_Process'] = process

    if ret['version'][0] == 5:
        ret['_KPCR_PrcbData'] = pdb.get_field_offset('_KPCR:PrcbData')

    return ret


def main():
    extract(get_info, 'gendriver.tpl')


if __name__ == '__main__':
    main()
