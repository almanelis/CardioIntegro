
from neurokit2.epochs import epochs_create, epochs_to_df
from neurokit2.signal import signal_rate, signal_formatpeaks
from neurokit2.ecg import ecg_peaks
from neurokit2.stats import standardize as nk_standardize
from neurokit2.ecg.ecg_delineate import _ecg_delineate_plot, _ecg_delineator_peak, _ecg_delineator_cwt, _dwt_ecg_delineator

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class CardioKit():
  def __init__(self) -> None:
    plt.rcParams ['figure.figsize'] = [16, 4]

  def events_plot(self, events, signal=None, show=True, color="red", linestyle="--", show_legend=True, save_fig=True, fig_name=""):
      """Plot events in signal.

      Parameters
      ----------
      events : list or ndarray or dict
          Events onset location. Can also be a list of lists, in which case it will mark them with
          different colors. If a dict is passed (e.g., from 'events_find()'), will select only the 'onset' list.
      signal : array or DataFrame
          Signal array (can be a dataframe with many signals).
      show : bool
          If True, will return a plot. If False, will return a DataFrame that can be plotted externally.
      color : str
          Argument passed to matplotlib plotting.
      linestyle : str
          Argument passed to matplotlib plotting.

      Returns
      -------
      fig
          Figure representing a plot of the signal and the event markers.

      See Also
      --------
      events_find

      Examples
      ----------
      >> import numpy as np
      >> import pandas as pd
      >> import neurokit2 as nk
      >>
      >> fig = nk.events_plot([1, 3, 5])
      >> fig #doctest: +SKIP
      >>
      >> # With signal
      >> signal = nk.signal_simulate(duration=4)
      >> events = nk.events_find(signal)
      >> fig1 = nk.events_plot(events, signal)
      >> fig1 #doctest: +SKIP
      >>
      >> # Different events
      >> events1 = events["onset"]
      >> events2 = np.linspace(0, len(signal), 8)
      >> fig2 = nk.events_plot([events1, events2], signal)
      >> fig2 #doctest: +SKIP
      >>
      >> # Conditions
      >> events = nk.events_find(signal, event_conditions=["A", "B", "A", "B"])
      >> fig3 = nk.events_plot(events, signal)
      >> fig3 #doctest: +SKIP
      >>
      >> # Different colors for all events
      >> signal = nk.signal_simulate(duration=20)
      >> events = nk.events_find(signal)
      >> events = [[i] for i in events['onset']]
      >> fig4 = nk.events_plot(events, signal)
      >> fig4 #doctest: +SKIP

      """

      if isinstance(events, dict):
          if "condition" in events.keys():
              events_list = []
              for condition in set(events["condition"]):
                  events_list.append([x for x, y in zip(events["onset"], events["condition"]) if y == condition])
              events = events_list
          else:
              events = events["onset"]

      if signal is None:
          signal = np.full(events[-1] + 1, 0)
      if isinstance(signal, pd.DataFrame) is False:
          signal = pd.DataFrame({"Signal": signal})

      # Plot if necessary
      if show:
          fig = signal.plot().get_figure()
          self._events_plot(events, color=color, linestyle=linestyle, show_legend=show_legend, save_fig=fig_name, fig_name=fig_name)
          return fig
      else:
          signal["Event_Onset"] = 0
          signal.iloc[events] = 1
          return signal


  def _events_plot(self, events, color="red", linestyle="--", show_legend=False, save_fig=True, fig_name=""):
      # Check if events is list of lists
      try:
          len(events[0])
          is_listoflists = True
      except TypeError:
          is_listoflists = False

      if is_listoflists is False:
          # Loop through sublists
          for event in events:
              plt.axvline(event, color=color, linestyle=linestyle)

          if show_legend:
            plt.legend()

          if save_fig:
            plt.savefig(fig_name)

      else:
          # Convert color and style to list
          if isinstance(color, str):
              color_map = matplotlib.cm.get_cmap("rainbow")
              color = color_map(np.linspace(0, 1, num=len(events)))
          if isinstance(linestyle, str):
              linestyle = np.full(len(events), linestyle)

          # Loop through sublists
          for i, event in enumerate(events):
              for j in events[i]:
                  plt.axvline(j, color=color[i], linestyle=linestyle[i], label=str(i))

          if show_legend:
              # Display only one legend per event type
              handles, labels = plt.gca().get_legend_handles_labels()
              newLabels, newHandles = [], []
              for handle, label in zip(handles, labels):
                  if label not in newLabels:
                      newLabels.append(label)
                      newHandles.append(handle)
              plt.legend(newHandles, newLabels)

          if save_fig:
            plt.savefig(fig_name)
      plt.close()


  def ecg_segment(self, ecg_cleaned, rpeaks=None, sampling_rate=500, show=False, show_legend=True, save_fig=False, fig_name=""):
      """Segment an ECG signal into single heartbeats.

      Parameters
      ----------
      ecg_cleaned : Union[list, np.array, pd.Series]
          The cleaned ECG channel as returned by `ecg_clean()`.
      rpeaks : dict
          The samples at which the R-peaks occur. Dict returned by
          `ecg_peaks()`. Defaults to None.
      sampling_rate : int
          The sampling frequency of `ecg_signal` (in Hz, i.e., samples/second).
          Defaults to 1000.
      show : bool
          If True, will return a plot of heartbeats. Defaults to False.

      Returns
      -------
      dict
          A dict containing DataFrames for all segmented heartbeats.

      See Also
      --------
      ecg_clean, ecg_plot

      Examples
      --------
      >>> import neurokit2 as nk
      >>>
      >>> ecg = nk.ecg_simulate(duration=15, sampling_rate=1000, heart_rate=80)
      >>> ecg_cleaned = nk.ecg_clean(ecg, sampling_rate=1000)
      >>> nk.ecg_segment(ecg_cleaned, rpeaks=None, sampling_rate=1000, show=True) #doctest: +ELLIPSIS
      {'1':              Signal  Index Label
      ...
      '2':              Signal  Index Label
      ...
      '19':              Signal  Index Label
      ...}

      """
      # Sanitize inputs
      if rpeaks is None:
          info, rpeaks = ecg_peaks(ecg_cleaned, sampling_rate=sampling_rate, correct_artifacts=True)
          rpeaks = rpeaks["ECG_R_Peaks"]

      epochs_start, epochs_end = self._ecg_segment_window(
        rpeaks=rpeaks, sampling_rate=sampling_rate, desired_length=len(ecg_cleaned)
      )

      heartbeats = epochs_create(
          ecg_cleaned, rpeaks, sampling_rate=sampling_rate, epochs_start=epochs_start, epochs_end=epochs_end
      )


      if show:
          heartbeats_plot = epochs_to_df(heartbeats)
          heartbeats_pivoted = heartbeats_plot.pivot(index="Time", columns="Label", values="Signal")
          plt.plot(heartbeats_pivoted)
          plt.xlabel("Time (s)")
          plt.title("Individual Heart Beats")
          cmap = iter(
              plt.cm.YlOrRd(np.linspace(0, 1, num=int(heartbeats_plot["Label"].nunique())))
          )  # pylint: disable=no-member
          lines = []
          for x, color in zip(heartbeats_pivoted, cmap):
              (line,) = plt.plot(heartbeats_pivoted[x], color=color)
              lines.append(line)

          if show_legend:
            plt.legend()

          if save_fig:
            plt.savefig(fig_name)
      plt.close()


      return heartbeats


  def _ecg_segment_window(self, heart_rate=None, rpeaks=None, sampling_rate=500, desired_length=None):

      # Extract heart rate
      if heart_rate is not None:
          heart_rate = np.mean(heart_rate)
      if rpeaks is not None:
          heart_rate = np.mean(signal_rate(rpeaks, sampling_rate=sampling_rate, desired_length=desired_length))

      # Modulator
      m = heart_rate / 60

      # Window
      epochs_start = -0.35 / m
      epochs_end = 0.5 / m

      # Adjust for high heart rates
      if heart_rate >= 80:
          c = 0.1
          epochs_start = epochs_start - c
          epochs_end = epochs_end + c

      return epochs_start, epochs_end



  def signal_plot(self, signal, sampling_rate=None, subplots=True, standardize=False, labels=None, show_legend=False, save_fig=True, fig_name="", **kwargs):
        """Plot signal with events as vertical lines.

        Parameters
        ----------
        signal : array or DataFrame
            Signal array (can be a dataframe with many signals).
        sampling_rate : int
            The sampling frequency of the signal (in Hz, i.e., samples/second). Needs to be supplied if
            the data should be plotted over time in seconds. Otherwise the data is plotted over samples.
            Defaults to None.
        subplots : bool
            If True, each signal is plotted in a subplot.
        standardize : bool
            If True, all signals will have the same scale (useful for visualisation).
        labels : str or list
            Defaults to None.
        **kwargs : optional
            Arguments passed to matplotlib plotting.

        Examples
        ----------
        >>> import numpy as np
        >>> import pandas as pd
        >>> import neurokit2 as nk
        >>>
        >>> signal = nk.signal_simulate(duration=10, sampling_rate=1000)
        >>> nk.signal_plot(signal, labels='signal1', sampling_rate=1000, color="red")
        >>>
        >>> data = pd.DataFrame({"Signal2": np.cos(np.linspace(start=0, stop=20, num=1000)),
        ...                      "Signal3": np.sin(np.linspace(start=0, stop=20, num=1000)),
        ...                      "Signal4": nk.signal_binarize(np.cos(np.linspace(start=0, stop=40, num=1000)))})
        >>> nk.signal_plot(data, labels=['signal_1', 'signal_2', 'signal_3'], subplots=False)
        >>> nk.signal_plot([signal, data], standardize=True)

        """
        # Sanitize format
        if isinstance(signal, list):
            try:
                for i in signal:
                    len(i)
            except TypeError:
                signal = np.array(signal)

        if isinstance(signal, pd.DataFrame) is False:
            # If list is passed
            if isinstance(signal, list) or (np.array(signal).shape[-1]<=12 and np.array(signal).shape[-1]>0):
                out = pd.DataFrame()
                for i, content in enumerate(signal):
                    if isinstance(content, (pd.DataFrame, pd.Series)):
                        out = pd.concat([out, content], axis=1, sort=True)
                    else:
                        out = pd.concat([out, pd.DataFrame({"Signal" + str(i + 1): content})], axis=1, sort=True)
                signal = out

            # If vector is passed
            else:
                signal = pd.DataFrame({"Signal": signal})

        # Copy signal
        signal = signal.copy()

        # Guess continuous and events columns
        continuous_columns = list(signal.columns.values)
        events_columns = []
        for col in signal.columns:
            vector = signal[col]
            if vector.nunique() == 2:
                indices = np.where(vector == np.max(vector.unique()))
                if bool(np.any(np.diff(indices) == 1)) is False:
                    events_columns.append(col)
                    continuous_columns.remove(col)

        # Adjust for sampling rate
        if sampling_rate is not None:
            signal.index = signal.index.astype(int) / sampling_rate
            title_x = "Time (seconds)"
    #        x_axis = np.linspace(0, signal.shape[0] / sampling_rate, signal.shape[0])
    #        x_axis = pd.DataFrame(x_axis, columns=["Time (s)"])
    #        signal = pd.concat([signal, x_axis], axis=1)
    #        signal = signal.set_index("Time (s)")


        # Plot accordingly
        if len(events_columns) > 0:
            events = []
            for col in events_columns:
                vector = signal[col]
                events.append(np.where(vector == np.max(vector.unique()))[0])
            plot = events_plot(events, signal=signal[continuous_columns])

            if sampling_rate is None:
                plot.gca().set_xlabel("Длительность")
            else:
                plot.gca().set_xlabel("Время (секунды)")

            if show_legend:
              plt.legend()
            if save_fig:
              plt.savefig(fig_name)


        else:
            if standardize is True:
                plot = nk_standardize(signal[continuous_columns]).plot(subplots=subplots, sharex=True, **kwargs)
                plot.get_legend().remove()
            else:
                plot = signal[continuous_columns].plot(subplots=subplots, sharex=True, **kwargs)
                plot.get_legend().remove()

            if sampling_rate is None:
                plt.xlabel("Длительность")
            else:
                plt.xlabel("Время (секунды)")

            if show_legend:
              plt.legend()
            if save_fig:
              plt.savefig(fig_name)


        # Tidy legend locations and add labels
        if labels is not None:

            if isinstance(labels, str):
                n_labels = len([labels])
                labels = [labels]
            elif isinstance(labels, list):
                n_labels = len(labels)

            if len(signal[continuous_columns].columns) != n_labels:
                raise ValueError("NeuroKit error: signal_plot(): number of labels does not equal the number of plotted signals.")

            if subplots is False:
                if show_legend:
                    plt.legend(labels, loc=1)
            else:
                if show_legend:
                    for i, label in enumerate(labels):
                        plot[i].legend([label], loc=1)
        plt.close()


  def ecg_delineate(self,
    ecg_cleaned,
    rpeaks=None,
    sampling_rate=1000,
    method="dwt",
    show=False,
    show_type="peaks",
    check=False,
    save_fig=False,
    fig_name = "",
    **kwargs
    ):
    """**Delineate QRS complex**

    Function to delineate the QRS complex, i.e., the different waves of the cardiac cycles. A
    typical ECG heartbeat consists of a P wave, a QRS complex and a T wave. The P wave represents
    the wave of depolarization that spreads from the SA-node throughout the atria. The QRS complex
    reflects the rapid depolarization of the right and left ventricles. Since the ventricles are
    the largest part of the heart, in terms of mass, the QRS complex usually has a much larger
    amplitude than the P-wave. The T wave represents the ventricular repolarization of the
    ventricles.On rare occasions, a U wave can be seen following the T wave. The U wave is believed
    to be related to the last remnants of ventricular repolarization.

    Parameters
    ----------
    ecg_cleaned : Union[list, np.array, pd.Series]
        The cleaned ECG channel as returned by ``ecg_clean()``.
    rpeaks : Union[list, np.array, pd.Series]
        The samples at which R-peaks occur. Accessible with the key "ECG_R_Peaks" in the info
        dictionary returned by ``ecg_findpeaks()``.
    sampling_rate : int
        The sampling frequency of ``ecg_signal`` (in Hz, i.e., samples/second). Defaults to 1000.
    method : str
        Can be one of ``"peak"`` for a peak-based method, ``"cwt"`` for continuous wavelet transform
        or ``"dwt"`` (default) for discrete wavelet transform.
    show : bool
        If ``True``, will return a plot to visualizing the delineated waves information.
    show_type: str
        The type of delineated waves information showed in the plot.
        Can be ``"peaks"``, ``"bounds_R"``, ``"bounds_T"``, ``"bounds_P"`` or ``"all"``.
    check : bool
        Defaults to ``False``. If ``True``, replaces the delineated features with ``np.nan`` if its
        standardized distance from R-peaks is more than 3.
    **kwargs
        Other optional arguments.

    Returns
    -------
    waves : dict
        A dictionary containing additional information.
        For derivative method, the dictionary contains the samples at which P-peaks, Q-peaks,
        S-peaks, T-peaks, P-onsets and T-offsets occur, accessible with the keys ``"ECG_P_Peaks"``,
        ``"ECG_Q_Peaks"``, ``"ECG_S_Peaks"``, ``"ECG_T_Peaks"``, ``"ECG_P_Onsets"``,
        ``"ECG_T_Offsets"``, respectively.

        For wavelet methods, in addition to the above information, the dictionary contains the
        samples at which QRS-onsets and QRS-offsets occur, accessible with the key
        ``"ECG_P_Peaks"``, ``"ECG_T_Peaks"``, ``"ECG_P_Onsets"``, ``"ECG_P_Offsets"``,
        ``"ECG_Q_Peaks"``, ``"ECG_S_Peaks"``, ``"ECG_T_Onsets"``, ``"ECG_T_Offsets"``,
        ``"ECG_R_Onsets"``, ``"ECG_R_Offsets"``, respectively.

    signals : DataFrame
        A DataFrame of same length as the input signal in which occurrences of
        peaks, onsets and offsets marked as "1" in a list of zeros.

    See Also
    --------
    ecg_clean, .signal_fixpeaks, ecg_peaks, .signal_rate, ecg_process, ecg_plot

    Examples
    --------
    * Step 1. Delineate

    .. ipython:: python

      import neurokit2 as nk

      # Simulate ECG signal
      ecg = nk.ecg_simulate(duration=10, sampling_rate=1000)
      # Get R-peaks location
      _, rpeaks = nk.ecg_peaks(ecg, sampling_rate=1000)
      # Delineate cardiac cycle
      signals, waves = nk.ecg_delineate(ecg, rpeaks, sampling_rate=1000)

    * Step 2. Plot P-Peaks and T-Peaks

    .. ipython:: python

      @savefig p_ecg_delineate1.png scale=100%
      nk.events_plot([waves["ECG_P_Peaks"], waves["ECG_T_Peaks"]], ecg)
      @suppress
      plt.close()

    References
    --------------
    - Martínez, J. P., Almeida, R., Olmos, S., Rocha, A. P., & Laguna, P. (2004). A wavelet-based
      ECG delineator: evaluation on standard databases. IEEE Transactions on biomedical engineering,
      51(4), 570-581.

    """
    # Sanitize input for ecg_cleaned
    if isinstance(ecg_cleaned, pd.DataFrame):
        cols = [col for col in ecg_cleaned.columns if "ECG_Clean" in col]
        if cols:
            ecg_cleaned = ecg_cleaned[cols[0]].values
        else:
            raise ValueError(
                "NeuroKit error: ecg_delineate(): Wrong input, we couldn't extract"
                "cleaned signal."
            )

    elif isinstance(ecg_cleaned, dict):
        for i in ecg_cleaned:
            cols = [col for col in ecg_cleaned[i].columns if "ECG_Clean" in col]
            if cols:
                signals = epochs_to_df(ecg_cleaned)
                ecg_cleaned = signals[cols[0]].values

            else:
                raise ValueError(
                    "NeuroKit error: ecg_delineate(): Wrong input, we couldn't extract"
                    "cleaned signal."
                )

    elif isinstance(ecg_cleaned, pd.Series):
        ecg_cleaned = ecg_cleaned.values

    # Sanitize input for rpeaks
    if rpeaks is None:
        _, rpeaks = ecg_peaks(ecg_cleaned, sampling_rate=sampling_rate)
        rpeaks = rpeaks["ECG_R_Peaks"]

    if isinstance(rpeaks, dict):
        rpeaks = rpeaks["ECG_R_Peaks"]

    method = method.lower()  # remove capitalised letters
    if method in ["peak", "peaks", "derivative", "gradient"]:
        waves = _ecg_delineator_peak(
            ecg_cleaned, rpeaks=rpeaks, sampling_rate=sampling_rate
        )
    elif method in ["cwt", "continuous wavelet transform"]:
        waves = _ecg_delineator_cwt(
            ecg_cleaned, rpeaks=rpeaks, sampling_rate=sampling_rate
        )
    elif method in ["dwt", "discrete wavelet transform"]:
        waves = _dwt_ecg_delineator(ecg_cleaned, rpeaks, sampling_rate=sampling_rate)

    else:
        raise ValueError(
            "NeuroKit error: ecg_delineate(): 'method' should be one of 'peak',"
            "'cwt' or 'dwt'."
        )

    # Ensure that all indices are not larger than ECG signal indices
    for _, value in waves.items():
        if value[-1] >= len(ecg_cleaned):
            value[-1] = np.nan

    # Remove NaN in Peaks, Onsets, and Offsets
    waves_noNA = waves.copy()
    for feature in waves_noNA.keys():
        waves_noNA[feature] = [
            int(x) for x in waves_noNA[feature] if ~np.isnan(x) and x > 0
        ]

    instant_peaks = signal_formatpeaks(waves_noNA, desired_length=len(ecg_cleaned))
    signals = instant_peaks

    waves_sanitized = {}
    for feature, values in waves.items():
        waves_sanitized[feature] = [x for x in values if x > 0 or x is np.nan]

    if show is True:
        fig = _ecg_delineate_plot(
            ecg_cleaned,
            rpeaks=rpeaks,
            signals=signals,
            signal_features_type=show_type,
            sampling_rate=sampling_rate,
            **kwargs
        )

        if save_fig:
            plt.savefig(fig_name)
        plt.close()

    if check is True:
        waves_sanitized = _ecg_delineate_check(waves_sanitized, rpeaks)

    return signals, waves_sanitized